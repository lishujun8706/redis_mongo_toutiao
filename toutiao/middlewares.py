# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import chardet,urllib,time
from selenium import webdriver

js='''
function scrollToBottom() {
    var Height = document.body.clientHeight,  //文本高度
        screenHeight = window.innerHeight,  //屏幕高度
        INTERVAL = 100,  // 滚动动作之间的间隔时间
        delta = 500,  //每次滚动距离
        curScrollTop = 0;    //当前window.scrollTop 值

    var scroll = function () {
        curScrollTop = document.body.scrollTop;
        window.scrollTo(0,curScrollTop + delta);
    };

    var timer = setInterval(function () {
        var curHeight = curScrollTop + screenHeight;
        if (curHeight >= Height){   //滚动到页面底部时，结束滚动
            clearInterval(timer);
        }
        scroll();
    }, INTERVAL)
}
'''

class ToutiaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class WebkitDownloaderTest( object ):
    def process_request( self, request, spider ):
#        if spider.name in settings.WEBKIT_DOWNLOADER:
#            if( type(request) is not FormRequest ):
        if not request.url.endswith('.jpg'):
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@'
            print urllib.unquote(request.url)
            driver = webdriver.PhantomJS()
            driver.get(request.url)
            driver.execute_script(js)
            time.sleep(10)  # 等待JS执行
            renderedBody=str(driver.page_source.encode('utf-8'))
            # browser = spynner.Browser()
            # browser.create_webview()
            # browser.set_html_parser(pyquery.PyQuery)
            # browser.load(urllib.unquote(request.url), 20)
            # try:
            #     browser.wait_load(20)
            # except:
            #     pass
            # string = browser.html
            # string=string.encode('utf-8')
            # renderedBody = str(string)
            print "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
            return HtmlResponse( request.url, body=renderedBody )
