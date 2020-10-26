# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  #影片名
    year = scrapy.Field()   #年份
    director = scrapy.Field()   #导演
    actor = scrapy.Field()  #演员
    area = scrapy.Field()   #地区
    type = scrapy.Field()   #类型
    score = scrapy.Field()  #评分
    pass
