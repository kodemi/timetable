from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
#from scrapy.contrib.loader import XPathItemLoader
from timetable.items import TimetableItem
from timetable.itemloaders import TimetableLoader

class VnukovoSpider(BaseSpider):
    name = "vnukovo.ru"
    allowed_domains = ["vnukovo.ru"]
    start_urls = [
        "http://vnukovo.ru/rus/for-passengers/board/index.wbp?time-table.direction=1",
        "http://vnukovo.ru/rus/for-passengers/board/index.wbp?time-table.direction=0"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        flights = hxs.select('//table[@id="TimeTable"]/tbody/tr')
        for flight in flights:
            loader = TimetableLoader(item=TimetableItem(), selector=flight)
            fields = ('flight', 'airline', 'airport_of_departure',
                    'airport_of_arrival', 'flight_status',
                    'datetime_scheduled', 'datetime_estimated',
                    'datetime_actual', 'terminal', 'comments')
            for idx, field in enumerate(fields, start=1):
                loader.add_xpath(field, 'td[%s]//text()' % idx)
            items.append(loader.load_item())
            #yield loader.load_item()
        return items
        """
        flights = hxs.select('//table[@id="TimeTable"]/tbody/tr')
        items = []
        for flight in flights:
            item = TimetableItem()
            fields = ('flight', 'airline', 'airport_of_departure',
                    'airport_of_arrival', 'flight_status',
                    'datetime_scheduled', 'datetime_estimated',
                    'datetime_actual', 'terminal', 'comments')
            for idx, field in enumerate(fields, start=1):
                item[field] = flight.select('td[%s]//text()' % idx).extract()
            items.append(item)
        return items
        """ 
