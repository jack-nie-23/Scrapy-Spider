# -*- coding: utf-8 -*-

# Scrapy settings for newsSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'newsSpider'

SPIDER_MODULES = ['newsSpider.spiders']
NEWSPIDER_MODULE = 'newsSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#用户代理
#作用是伪装，将爬虫访问伪装成浏览器进行访问
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False   #爬虫协议，即robots协议.默认为true
REDIS_HOST = 'xx.xx.xx.xx'  # 主机名
REDIS_PORT = 6379  # 端口
REDIS_PARAMS = {'password': 'xxxx'}    #scrapy-redis的redis密码配置
BLOOMFILTER_HASH_NUMBER = 6  #布隆过滤器，hash函数的使用数量
BLOOMFILTER_BIT = 31        #Bloom Filter的bit参数
SCHEDULER_PERSIST = True  #不清除Redis队列、这样可以暂停/恢复 爬取
DEPTH_LIMIT = 5            #爬取深度限制
#所谓的深度爬取则是在只抓取一个url的情况下获取该页面上其他页面的链接，然后将这些url加入到urljoin（）中进行一一爬取

# CONCURRENT_REQUESTS = 16

# DOWNLOAD_DELAY = 4
#下载器中间件（禁止内置的中间件-->是为了反爬虫）
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}
#为了启用Item Pipeline组件，必须将它的类添加到 settings.py文件ITEM_PIPELINES 配置
ITEM_PIPELINES = {
    'newsSpider.pipelines.MysqlPipeline': 300,
    # 'newsSpider.pipelines.MongoDBPipeline': 300,
}

# LOCAL_MONGO_HOST = '192.168.1.103'
# LOCAL_MONGO_PORT = 27017pwd
# DB_NAME = 'news'

#数据存在数据库服务器上
MYSQL_HOST = 'xx.xx.xx.xx'
MYSQL_DBNAME = 'xx'  # 数据库名字，请修改
MYSQL_USER = 'xx'  # 数据库账号，请修改
MYSQL_PASSWD = 'xx'  # 数据库密码，请修改
MYSQL_PORT = 3306  # 数据库端口，在dbhelper中使用

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'newsSpider.middlewares.NewsspiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'newsSpider.middlewares.NewsspiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'newsSpider.pipelines.NewsspiderPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'