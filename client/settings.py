# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'client'

SPIDER_MODULES = ['client.spiders']
NEWSPIDER_MODULE = 'client.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

# FEED_URI = 'stdout:'
# FEED_FORMAT = 'json'
# FEED_STORAGES_BASE = {
#     'stdout': 'scrapy.contrib.feedexport.StdoutFeedStorage'
# }
#
# FEED_EXPORTERS_BASE = {
#     'json': 'scrapy.contrib.exporter.JsonItemExporter'
# }

ITEM_PIPELINES = {
    'client.pipelines.JsonWriterPipeline': 100,
}