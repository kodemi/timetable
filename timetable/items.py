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
        date_list = value.split()
        if len(date_list) == 2:
            try:
                value = datetime.strptime(value, "%H:%M %d.%m").replace(
                    year=datetime.now().year)
            except ValueError:
                value = datetime.strptime(value, "%d.%m %H:%M").replace(
                    year=datetime.now().year)
        elif len(date_list) == 1:
            value = datetime.strptime(value, "%H:%M").replace(
                year=datetime.now().year)
        else:
            value = datetime.strptime(date_list[2], "%H:%M").replace(
                year=datetime.now().year, month=datetime.now().month, day=int(date_list[0]))
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
    city_of_departure = Field()
    airport_of_arrival = Field()
    city_of_arrival = Field()
    flight_status = Field()
    datetime_scheduled = Field(output_processor=Compose(Join(), to_datetime))
    datetime_estimated = Field(output_processor=Compose(Join(), to_datetime), default=None)
    datetime_actual = Field(output_processor=Compose(Join(), to_datetime), default=None)
    terminal = Field()
    comment = Field()
    checkin_desk = Field(output_processor=Compose(Join(), checkin_desk_processor))

