from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from timetable.items import TimetableItem
from timetable.itemloaders import TimetableLoader

class VnukovoSpider(BaseSpider):
    name = "vnukovo.ru"
    allowed_domains = ["vnukovo.ru"]
    start_urls = [
        "http://vnukovo.ru/rus/for-passengers/board/index.wbp?time-table.direction=0",
        "http://vnukovo.ru/rus/for-passengers/board/index.wbp?time-table.direction=1",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        # flight_type: 0 - arrival; 1 - departure
        flight_type = 0 if response.request.url == self.start_urls[0] else 1
        items = []
        flights = hxs.select('//table[@id="TimeTable"]/tbody/tr')
        for flight in flights[:2]:
            loader = TimetableLoader(item=TimetableItem(), selector=flight)
            fields = ('flight', 'airline', 'airport_of_departure',
                    'airport_of_arrival', 'flight_status',
                    'datetime_scheduled', 'datetime_estimated',
                    'datetime_actual', 'terminal')
            for idx, field in enumerate(fields, start=1):
                loader.add_xpath(field, 'td[%s]//text()' % idx)
            fields = ('checkin_desk', 'comment')
            field_xpath, field_value = fields if flight_type else (fields[1], fields[0])
            loader.add_xpath(field_xpath, 'td[10]//text()')
            loader.add_value('airport', u'VKO')
            item = loader.load_item()
            item[field_value] = u''
            item['flight_type'] = flight_type
            items.append(item)
            #yield loader.load_item()
        return items
