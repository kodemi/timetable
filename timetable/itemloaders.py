from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

class TimetableLoader(XPathItemLoader):
   default_output_processor = Join()
   default_input_processor = MapCompose(unicode.strip)
