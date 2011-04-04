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
    try:
        if len(value.split()) == 2:
            value = datetime.strptime(value, "%H:%M %d.%m").replace(
                year=datetime.now().year)
        else:
            value = datetime.strptime(value, "%H:%M").replace(
                year=datetime.now().year)
    except ValueError:
        return None
    return value

def checkin_desk_processor(value):
    if value == '0':
        return ''
    else:
        return value

class TimetableItem(Item):
    airport = Field()
    flight_type = Field()
    flight = Field()
    airline = Field()
    airport_of_departure = Field()
    airport_of_arrival = Field()
    flight_status = Field()
    datetime_scheduled = Field(output_processor=Compose(Join(), to_datetime))
    datetime_estimated = Field(output_processor=Compose(Join(), to_datetime))
    datetime_actual = Field(output_processor=Compose(Join(), to_datetime))
    terminal = Field()
    comment = Field()
    checkin_desk = Field(output_processor=Compose(Join(), checkin_desk_processor))

