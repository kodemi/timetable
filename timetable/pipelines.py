#-*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log
from scrapy.conf import settings
from scrapy.contrib.exporter import BaseItemExporter
from twisted.enterprise import adbapi
import MySQLdb.cursors
from restful_lib import Connection
import json


class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db=settings.get('DATABASE_NAME'),
                user=settings.get('DATABASE_USER'),
                passwd=settings.get('DATABASE_PASSWORD'),
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
            )

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute("select * from timetable_vnukovo where flight = %s", (item['flight'],))
        result = tx.fetchone()
        if result:
            query = [] 
            for field in item.keys():
                if item[field] is None:
                    query.append("%s is Null" % field)
                else:
                    query.append("%s = '%s'" % (field, item[field]))
            query = ' and '.join(query)
            query = ' '.join(("select * from timetable_vnukovo where", query))
            tx.execute(query)
            result = tx.fetchone()
            if result:
                log.msg("Item already stored in db", level=log.DEBUG)
            else:
                tx.execute(
                    "update timetable_vnukovo set "
                    "flight_status = %s, "
                    "datetime_scheduled = %s, "
                    "datetime_estimated = %s, "
                    "datetime_actual = %s, "
                    "comment = %s "
                    "where flight = %s", (
                        item['flight_status'],
                        item['datetime_scheduled'],
                        item['datetime_estimated'], 
                        item['datetime_actual'],
                        item['comment'],
                        item['flight'] 
                    )
                )
                log.msg("Item updated in db", level=log.DEBUG)
        else:
            tx.execute(
                "insert into timetable_vnukovo (flight, flight_type, "
                "airline, airport_of_departure, "
                "airport_of_arrival, flight_status, "
                "datetime_scheduled, datetime_estimated, "
                "datetime_actual, terminal, comment) "
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    item['flight'], 
                    item['flight_type'], 
                    item['airline'], 
                    item['airport_of_departure'],
                    item['airport_of_arrival'], 
                    item['flight_status'],
                    item['datetime_scheduled'], 
                    item['datetime_estimated'],
                    item['datetime_actual'], 
                    item['terminal'], 
                    item['comment']
                )
            )
            log.msg("Item stored in db", level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)


class RestPipeline(object):
    def __init__(self):
        base_url = settings.get('API_BASE_URL')
        self.conn = Connection(base_url)

    def process_item(self, item, spider):
        data = dict(item.items())
        for k in data:
            if k in ('datetime_scheduled', 'datetime_estimated', 'datetime_actual'):
                if data[k]:
                    data[k] = data[k].isoformat(' ')
                else:
                    data[k] = None
            elif k == 'flight_type':
                continue
            else:
                data[k] = data[k].encode('utf-8')
        data = json.dumps(data)
        resp = self.conn.request_post("/flights", args={'data': data})
        #log.msg('Response: %s' % resp, level=log.DEBUG)
        return item

