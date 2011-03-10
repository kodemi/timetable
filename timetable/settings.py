# Scrapy settings for timetable project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'timetable'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['timetable.spiders']
NEWSPIDER_MODULE = 'timetable.spiders'
DEFAULT_ITEM_CLASS = 'timetable.items.TimetableItem'
ITEM_PIPELINES = ['timetable.pipelines.TimetablePipeline']
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

