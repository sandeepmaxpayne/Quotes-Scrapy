# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader
from cote_spider.items import CoteSpiderItem

from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser



class QuotesSpider(Spider):
    name = 'quot'
   # allowed_domains = ['quotes.toscrap.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        print("token:{}".format(token))
        return FormRequest.from_response(response, formdata={"csrf_token": token,
                                                            "username": 'abcd',
                                                            "password": '123456'
                                                            },
                                                            callback=self.login_page)

    def login_page(self, response):
        open_in_browser(response)
        l = ItemLoader(item=CoteSpiderItem(), response=response)
        h_tag = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        
        l.add_value('h1_tag', h_tag) # key value need to be same as of items
        l.add_value('tag', tags)

        return l.load_item()

        
        