# -*- coding: utf-8 -*-

# Scrapy settings for SpiderYM project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'SpiderYM'

SPIDER_MODULES = ['SpiderYM.spiders']
NEWSPIDER_MODULE = 'SpiderYM.spiders'

ROBOTSTXT_OBEY = False

'''
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/49.0.2623.87 Safari/537.36'
'''

# 配置默认的请求头
DEFAULT_REQUEST_HEADERS = {
    "User-Agent" : "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
# 配置使用Pipeline
ITEM_PIPELINES = {
    'SpiderYM.pipelines.SpiderymPipeline': 300,
}

#LOG_LEVEL = 'WARNING'
#LOG_FILE = './log.log'