# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import DmozItem

from scrapy.spiders import CrawlSpider, Request, Rule
from scrapy.linkextractors import LinkExtractor

class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['imdb.cn']
    start_urls = ['https://www.im'
                  ''
                  'db.cn/movies/']
    base_site = 'https://www.imdb.cn/movies/'
    host = "https://www.imdb.cn/"
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0"
    }

    def parse(self,response):
        lists = response.css(".hot_box  .hot_list li ")
        for index,list in enumerate(lists):
            url = list.css(".img_title::attr(href)").extract()
            url = self.host + url[0]
            yield scrapy.Request(url, callback=self.parse_item,headers=self.headers)

        for pi in range(1, 400):
            url = "https://www.imdb.cn/movies/?page="+str(pi)
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)


    def parse_item(self, response):
        item = DmozItem()
        item["title"] = response.xpath("//div[@class='per_txt fr']/h1/div/text()").extract()[0].strip()   #影片名 , strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列,也可用normalize-space()即可去掉所有空白符
        item["year"] = response.xpath('.//h1/div/span/text()').extract()[0].strip('(').strip(')')  #年份
        item["director"] = response.xpath('//div[@class="txt_bottom_r txt_bottom_r_overflow"]/a/text()').get()# 导演
        item["actor"] = ','.join(response.xpath("(//div[@class='txt_bottom_r txt_bottom_r_overflow'])[last()]/a/text()").getall())  # 演员
        item["score"] = response.xpath('//span/em/text()').extract()[0].strip()    #分数

        inform = response.xpath('//div[@class="txt_bottom_r"]/text()').getall()

        item["type"] = (inform[0].strip()).replace(' ', '')  # 类型
        item["area"] = inform[1].strip()  # 国家/地区


        print(item)
        yield item;




