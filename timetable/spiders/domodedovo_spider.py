from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from timetable.items import TimetableItem
from timetable.itemloaders import TimetableLoader
import re

class DomodedovoSpider(BaseSpider):
    name = "domodedovo.ru"
    allowed_domains = ["domodedovo.ru"]
    start_urls = [
        "http://www.domodedovo.ru/ru/main/airindicator/arrivalnew/",
        "http://www.domodedovo.ru/ru/main/airindicator/flightnew/",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        # flight_type: 0 - arrival; 1 - departure
        flight_type = 0 if response.request.url == self.start_urls[0] else 1
        items = []
        flights = hxs.select('//table[@id="set"]/tr[position() != last()]')
        for flight in flights:
            item = next(self.parse_main_contents(flight, response, flight_type))
            items.append(item)
        return items

    def parse_main_contents(self, flight, response, flight_type):
        loader = TimetableLoader(item=TimetableItem(), selector=flight)
        loader.add_xpath('flight', 'td[1]//text()')
        loader.add_xpath('datetime_scheduled', 'td[3]//text()')
        loader.add_xpath('datetime_actual', 'td[4]//text()')
        loader.add_xpath('flight_status', 'td[6]//text()')
        loader.add_value('airport', u'DME')
        loader.add_value('flight_type', flight_type)
        loader.add_value('terminal', u'')
        item = loader.load_item()
        details = re.findall(r'\w+', flight.select('@onclick').extract()[0])[1]
        url = 'http://www.domodedovo.ru/ru/main/airindicator/detailsnew2.asp?id=%s' % details
        request = Request(url, callback = lambda r: self.parse_url_contents(r))
        request.meta['item'] = item
        yield request

    def parse_url_contents(self, response):
        hxs = HtmlXPathSelector(response)
        item = response.request.meta['item']
        xpaths = ('/html/body/table[1]/tr[3]/td/table[2]/tr[6]/td[2]/text()',
            '/html/body/table[1]/tr[3]/td/table[2]/tr[7]/td[2]/text()',
            '/html/body/table[1]/tr/td/table[2]/tr[6]/td[2]/text()',
            '/html/body/table[1]/tr[3]/td/table[2]/tr[7]/td[2]/text()')
        for xpath in xpaths:
            flight_route = hxs.select(xpath)
            if flight_route:
                flight_route = flight_route.extract()[0]
                break
        flight_route = flight_route.split('-&gt;')
        if len(flight_route) == 2:
            departure, arrival = flight_route
        else:
            departure, arrival = flight_route[0], flight_route[-1]
        for direction in [(departure, 'departure'), (arrival, 'arrival')]:
            city_airport = re.findall(r'(\w+)', direction[0], re.U)
            if len(city_airport) == 2:
                item['city_of_%s' % direction[1]], item['airport_of_%s' % direction[1]] = city_airport
            else:
                item['city_of_%s' % direction[1]] = city_airport[0]
        airline = hxs.select('/html/body/table[1]/tr[3]/td/table[2]/tr[4]/td[2]//text()')
        if not airline:
            airline = hxs.select('/html/body/table[1]/tr/td/table[2]/tr[4]/td[2]//text()')
        item['airline'] = airline.extract()[0]
        yield item