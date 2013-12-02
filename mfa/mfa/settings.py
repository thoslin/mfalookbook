# Scrapy settings for mfa project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mfa'

SPIDER_MODULES = ['mfa.spiders']
NEWSPIDER_MODULE = 'mfa.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1'

DOWNLOAD_DELAY = 10

ITEM_PIPELINES = {
    'mfa.pipelines.MfaPipeline': 100,
}