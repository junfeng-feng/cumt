# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DianpingItem(scrapy.Item):
    # define the fields for your item here like:

    accidentId = scrapy.Field()
    
    accidentName = scrapy.Field()
    country = scrapy.Field()
    province = scrapy.Field()
    accidentClass = scrapy.Field()
    accidentType = scrapy.Field()
    accidentDate = scrapy.Field()  


    accidentDescription = scrapy.Field()     
    pass
