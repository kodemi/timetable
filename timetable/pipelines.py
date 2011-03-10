#-*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import PprintItemExporter, BaseItemExporter

class TimetableItemExporter(BaseItemExporter):
    def __init__(self, file=file, *args, **kwargs):

        self.file = file 
        super(TimetableItemExporter, self).__init__(*args, **kwargs)

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
        self.exporter = TimetableItemExporter(file=file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
