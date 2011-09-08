#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from timetable.items import TimetableItem
from timetable.itemloaders import TimetableLoader
from datetime import datetime
import re

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
        for flight in flights:
            item = next(self.parse_main_contents(flight, response))
            items.append(item)
        return items

    def parse_main_contents(self, flight, response):
        # flight_type: 0 - arrival; 1 - departure
        flight_type = flight.select('@class').extract()[0].split()
        flight_type = 0 if 'sA' in flight_type else 1
        loader = TimetableLoader(item=TimetableItem(), selector=flight)
        loader.add_xpath('flight', 'td[2]//text()')
        loader.add_xpath('airline', 'td[3]//@alt')
        loader.add_xpath('flight_status', 'td[5]//text()')
        loader.add_xpath('datetime_scheduled', 'td[7]//text()')
        loader.add_xpath('datetime_estimated', 'td[8]//text()')
        loader.add_xpath('datetime_actual', 'td[9]//text()')
        loader.add_xpath('terminal', 'td[10]//text()')
        loader.add_value('airport', u'SVO')
        item = loader.load_item()
        nowdate = datetime.date(datetime.now())
        item['datetime_scheduled'] = item['datetime_scheduled'].replace(
                month=nowdate.month, day=nowdate.day)
        if item['datetime_estimated']:
            item['datetime_estimated'] = item['datetime_estimated'].replace(
                month=nowdate.month, day=nowdate.day)
        if item['datetime_actual']:
            item['datetime_actual'] = item['datetime_actual'].replace(
                month=nowdate.month, day=nowdate.day)
        item['flight_type'] = flight_type

        url = 'http://svo.aero%s' % (flight.select('td[2]//a/@href').extract()[0])
        request = Request(url, callback = lambda r: self.parse_url_contents(r))
        request.meta['item'] = item
        yield request


    def parse_url_contents(self, response):
        hxs = HtmlXPathSelector(response)
        flight_route = hxs.select('//div[@class="content"]/table/tr[5]/td[2]/text()').extract()[0]
        routes = flight_route.split(u'\u2192')
        departure, arrival = routes[0], routes[-1]
        item = response.request.meta['item']
        #print departure, re.findall(r'[^\(\)]+', departure, re.U)
        item['city_of_departure'], item['airport_of_departure'] = [x.strip() for x in re.findall(r'[^\(\)]+', departure.strip(), re.U)[:2]]
        item['city_of_arrival'], item['airport_of_arrival'] = [x.strip() for x in re.findall(r'[^\(\)]+', arrival.strip(), re.U)[:2]]
        yield item
