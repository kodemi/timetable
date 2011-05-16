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
ITEM_PIPELINES = [#'timetable.pipelines.TimetablePipeline',
        #'timetable.pipelines.MySQLStorePipeline']
        'timetable.pipelines.RestPipeline']
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'

DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''

API_BASE_URL = 'http://localhost:8000/api'
