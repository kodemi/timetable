# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import Compose, Join
from datetime import datetime

def to_datetime(value):
    if value == '-':
        return None
    value = datetime.strptime(value, "%H:%M %d.%m").replace(
            year=datetime.now().year)
    return value

class TimetableItem(Item):
    flight = Field()
    airline = Field()
    airport_of_departure = Field()
    airport_of_arrival = Field()
    flight_status = Field()
    datetime_scheduled = Field(output_processor=Compose(Join(), to_datetime))
    datetime_estimated = Field(output_processor=Compose(Join(), to_datetime))
    datetime_actual = Field(output_processor=Compose(Join(), to_datetime))
    terminal = Field()
    comments = Field()

