
# encoding=utf-8
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging
import json
import copy
import time
import uuid
import sys

from dianping.items import DianpingItem

# logging.basicConfig(level=logging.INFO,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='dianping.log',
#                 filemode='a')

class SpiderTmallShop(Spider):
    name = 'dianping'
    
    allowed_domain = ['dinaping.com']
    start_urls = []
    for pageNo in range(1, 3200):
        start_urls.append("http://accident.nrcc.com.cn:9090/Portalsite/SearchResult.aspx?pmenu=27876dcf-10d8-41d2-897c-67ff37286e9a&menu=540e49bb-4442-4f48-97fd-9decfb5a7e2a&pagenum=%s&sgk=&sgmc=%%E8%%BD%%A6&begindate=&enddate=&gnw=780c35e4-3565-435f-bc11-bf4605b8e2a2&sheng=&shi=&qx=&wzmc=&sglx=&sgbk=&sgjb=&czjd=&gylx=&sbzz=&sfhj=&qymc=&qyxz=&swrs1=&swrs2=&param=" % (pageNo))
        
    def __init__(self):
        pass
    
    def parse(self, response):
   
        select = Selector(response)

        item = DianpingItem()
        trList = select.xpath(""".//div[@id="wrapper"]//div[@class='con_sea_end']//tr""")  
        for  tr in trList[1:]:  #[1:]跳过标题行
            item["accidentName"] = tr.xpath(".//a/text()").extract()[0]
            item["country"] = tr.xpath(".//td[2]/text()").extract()[0]
            item["province"] = tr.xpath(".//td[3]/text()").extract()[0]
            item["accidentClass"] = tr.xpath(".//td[4]/text()").extract()[0]
            item["accidentType"] = tr.xpath(".//td[5]/text()").extract()[0]
            item["accidentDate"] = tr.xpath(".//td[6]/text()").extract()[0]

            descUrl = """http://accident.nrcc.com.cn:9090/Portalsite/""" + tr.xpath(".//a/@href").extract()[0]
            request = Request(descUrl, callback=self.parseDescription, priority=1234)#店铺请求
            request.meta["accident"] = copy.deepcopy(item)
            #print(item)
            yield request
            
        pass
            

    def parseDescription(self, response):
        #item['accidentDescription'] = select.xpaht("""//*[@id="wrapper"]/div[3]/div[1]/div[2]/div[3]/div/p[1]""").extract()
        #print("parseDescription----")
        item = response.meta['accident']
        index = response.url.find("id=")
        item['accidentId'] = response.url[index+3:]

        select = Selector(response)
        desc = ""
        pTextList =select.css(".content_text").xpath("//p/text()")
        for pText in pTextList[:-2]:
            desc = desc + pText.extract()
        item["accidentDescription"] = desc
        yield item
        pass

