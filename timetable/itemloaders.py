from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, Compose, MapCompose, Identity

def return_first(value):
	return value[0]

class TimetableLoader(XPathItemLoader):
   default_output_processor = Join()
   default_input_processor = MapCompose(unicode.strip)
#   flight_type_in = Identity()
#   flight_type_out = Compose(return_first)
