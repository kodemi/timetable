#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from timetable.items import TimetableItem
from timetable.itemloaders import TimetableLoader
import re

class PulkovoSpider(BaseSpider):
    name = "pulkovoairport.ru"
    allowed_domains = ["pulkovoairport.ru"]
    start_urls = [
        "http://www.pulkovoairport.ru/online_serves/online_timetable/arrivals/?p=1",
        #"http://www.pulkovoairport.ru/online_serves/online_timetable/arrivals/?p=2",
        #"http://www.pulkovoairport.ru/online_serves/online_timetable/departures/?p=1",
        #"http://www.pulkovoairport.ru/online_serves/online_timetable/departures/?p=2"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        # flight_type: 0 - arrival; 1 - departure
        flight_type = 0 if response.request.url in self.start_urls[:2] else 1
        items = []
        flights = hxs.select('//table[@class="tablo tabloBigNew bigTableZebra"]/tr[position() != 1 and position() != 8]')
        for flight in flights[:10:2]:
            loader = TimetableLoader(item=TimetableItem(), selector=flight)
            loader.add_xpath('flight', 'td[1]//text()')
            loader.add_xpath('datetime_scheduled', 'td[3]//text()')
            loader.add_xpath('datetime_actual', 'td[4]//text()')
            loader.add_xpath('flight_status', 'td[5]//text()')
            loader.add_xpath('airline', 'td[6]//text()')
            city_airport = flight.select('td[2]//text()').extract()[0]
            city_airport = re.findall(r'[^\(\)]+', city_airport, re.U)
            if len(city_airport) == 2:
                city, airport = city_airport
            else:
                city, airport = city_airport[0], u''
            if flight_type:
                loader.add_value('city_of_arrival', city)
                loader.add_value('airport_of_arrival', airport)
                loader.add_value('city_of_departure', u'Санкт-Петербург')
                loader.add_value('airport_of_departure', u'Пулково')
            else:
                loader.add_value('city_of_departure', city)
                loader.add_value('airport_of_departure', airport)
                loader.add_value('city_of_arrival', u'Санкт-Петербург')
                loader.add_value('airport_of_arrival', u'Пулково')
            loader.add_value('terminal', response.request.url[-1:].decode('utf-8'))
            loader.add_value('airport', u'LED')
            item = loader.load_item()
            items.append(item)
        return items
        