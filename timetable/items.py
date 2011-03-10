# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TimetableItem(Item):
    flight = Field()
    airline = Field()
    airport_of_departure = Field()
    airport_of_arrival = Field()
    flight_status = Field()
    datetime_scheduled = Field()
    datetime_estimated = Field()
    datetime_actual = Field()
    terminal = Field()
    comments = Field()

