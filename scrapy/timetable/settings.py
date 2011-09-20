# Scrapy settings for timetable project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

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
SELECTORS_BACKEND = 'lxml'
LOG_FILE = os.path.join(PROJECT_DIR, 'log.log')
LOG_LEVEL = 'WARNING'

RETRY_ENABLES = True
RETRY_TIMES = 3
DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 10
#AUTOTHROTTLE_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': None,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    #'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': None,
}

TELNETCONSOLE_ENABLED = False
WEBSERVICE_ENABLED = False