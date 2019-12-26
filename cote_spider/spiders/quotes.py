# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrap.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # h_tag = response.xpath('//h1/a/text()').extract_first()
        # tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        # yield {'H1 Tag': h_tag, 'Tag': tags}
        quotes = response.xpath("//*[@class='quote']")
        for quote in quotes:
            tag = quote.xpath(".//*[@itemprop='keywords']/@content").extract_first()       
            author = quote.xpath(".//*[@itemprop='author']/text()").extract_first()   
            text = quote.xpath(".//*[@itemprop='text']/text()").extract_first()

#            print(f"tag: {tag}\nauthor: {author}\ntext: {text}")
 #           print("\n")
            yield{
                'text': text,
                'author': author,
                'tag': tag
            }
        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first() 
        absolute_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_url)