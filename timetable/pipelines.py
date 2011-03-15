#-*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import BaseItemExporter
from twisted.enterprise import adbapi
import MySQLdb.cursors

class PrintItemExporter(BaseItemExporter):
    def __init__(self, file=file, *args, **kwargs):
        self.file = file 
        super(PrintItemExporter, self).__init__(*args, **kwargs)

    def export_item(self, item):
        string = u"\n".join([u"{0}: {1}".format(k, v) for k,v in item.items()]).encode('utf-8')
        self.file.write(string)    
        self.file.write('\n\n')

class TimetablePipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('%s_flights' % spider.name, 'w')
        self.files[spider] = file
        self.exporter = PrintItemExporter(file=file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db='timetable',
                user='root',
                passwd='n5hgcb-jhf',
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
                    "comments = %s "
                    "where flight = %s", (
                        item['flight_status'],
                        item['datetime_scheduled'],
                        item['datetime_estimated'], 
                        item['datetime_actual'],
                        item['comments'],
                        item['flight'] 
                    )
                )
                log.msg("Item updated in db", level=log.DEBUG)
        else:
            tx.execute(
                "insert into timetable_vnukovo (flight, airline, airport_of_departure, "
                "airport_of_arrival, flight_status, datetime_scheduled, datetime_estimated, "
                "datetime_actual, terminal, comments) "
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    item['flight'], 
                    item['airline'], 
                    item['airport_of_departure'],
                    item['airport_of_arrival'], 
                    item['flight_status'],
                    item['datetime_scheduled'], 
                    item['datetime_estimated'],
                    item['datetime_actual'], 
                    item['terminal'], 
                    item['comments']
                )
            )
            log.msg("Item stored in db", level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
