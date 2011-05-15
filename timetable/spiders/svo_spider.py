#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from timetable.items import TimetableItem
from timetable.itemloaders import TimetableLoader
from datetime import datetime

SVO = u'Москва(Шереметьево)'

class SvoSpider(BaseSpider):
    name = "svo.aero"
    allowed_domains = ["svo.aero"]
    start_urls = [
        "http://www.svo.aero/timetable/today/",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        flights = hxs.select('//div[@class="table"]/table/tbody/tr')
        for flight in flights[:2]:
            # flight_type: 0 - arrival; 1 - departure
            flight_type = flight.select('@class').extract()[0].split()
            flight_type = 0 if 'sA' in flight_type else 1
            loader = TimetableLoader(item=TimetableItem(), selector=flight)
            if flight_type:
                loader.add_xpath('airport_of_arrival', 'td[4]//text()')
                loader.add_value('airport_of_departure', SVO)
            else:
                loader.add_xpath('airport_of_departure', 'td[4]//text()')
                loader.add_value('airport_of_arrival', SVO)
            loader.add_xpath('flight', 'td[2]//text()')
            loader.add_xpath('airline', 'td[3]//@alt')
            loader.add_xpath('flight_status', 'td[5]//text()')
            loader.add_xpath('datetime_scheduled', 'td[7]//text()')
            loader.add_xpath('datetime_estimated', 'td[8]//text()')
            loader.add_xpath('datetime_actual', 'td[9]//text()')
            loader.add_xpath('terminal', 'td[10]//text()')
            loader.add_value('airport', u'SVO')
            loader.add_value('city_of_departure', u'')
            loader.add_value('city_of_arrival', u'')
            item = loader.load_item()
            nowdate = datetime.date(datetime.now())
            item['datetime_scheduled'] = item['datetime_scheduled'].replace(
                    month=nowdate.month, day=nowdate.day)
            item['datetime_estimated'] = item['datetime_estimated'].replace(
                    month=nowdate.month, day=nowdate.day)
            item['datetime_actual'] = item['datetime_actual'].replace(
                    month=nowdate.month, day=nowdate.day)
            item['flight_type'] = flight_type
            items.append(item)
            #yield loader.load_item()
        return items
