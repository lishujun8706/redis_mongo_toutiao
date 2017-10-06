# -*- coding: utf-8 -*-
import scrapy
import datetime
from ..items import ToutiaoHistory
from scrapy.spider import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisSpider

class ToutiaoImgSpider(RedisSpider):
    name = 'toutiao_imggg'
    allowed_domains = ['toutiao.com']
    redis_key = 'toutiaospider:start_urls'
    #start_urls = ['http://www.toutiao.com/ch/news_history/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="link title"]'),callback='parse_item',follow=True),
    )

    def parse(self, response):
        print '==================================='
        print 'this is parse'
        links = response.xpath('//a[@class="link title"]/@href').extract()
        for url in links:
            yield Request(url='http://www.toutiao.com' + url,callback=self.parse_item)

    def parse_item(self,response):
        print '==================================='
        print 'this is parse_item'
        contents = response.xpath('//div[@class="article-content"]/div/p/text()').extract()
        title = response.xpath('//h1[@class="article-title"]/text()').extract()
        # for cts in contents:
        thistory = ToutiaoHistory()
        thistory['title'] = title
        string = ''
        for i in contents:
            string += i
        print string
        print "||||||||||||||||||||||||||||||||||||||||||"
        thistory['content'] = string
        thistory['datetime'] = datetime.datetime.now()
        return thistory