
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
    for pageNo in range(1, 2700):
        start_urls.append("http://accident.nrcc.com.cn:9090/Portalsite/SearchResult.aspx?pmenu=27876dcf-10d8-41d2-897c-67ff37286e9a&menu=540e49bb-4442-4f48-97fd-9decfb5a7e2a&pagenum=%s&sgk=&sgmc=&begindate=&enddate=&gnw=&sheng=&shi=&qx=&wzmc=&sglx=&sgbk=&sgjb=&czjd=&gylx=&sbzz=&sfhj=&qymc=&qyxz=&swrs1=&swrs2=&param=" % (pageNo))
        
    def __init__(self):
        self.hourRe = re.compile("([1-9]|[0-9]{1,2}) *(时|点)")
        self.noonRe = re.compile("上午|下午|凌晨|早上|晚上|清早|傍晚|深夜|夜里|正午|黄昏")
        pass
    
    def parse(self, response):
   
        select = Selector(response)

        item = DianpingItem()
        item["accidentName"] = ""
        item["country"] = ""
        item["province"] = ""
        item["accidentClass"] = ""
        item["accidentType"] = ""
        item["accidentDate"] = ""
        item['accidentNoon']= ""
        item["accidentHour"] = ""
        item["accidentDescription"] = ""

        trList = select.xpath(""".//div[@id="wrapper"]//div[@class='con_sea_end']//tr""")  
        for  tr in trList[1:]:  #[1:]跳过标题行
            try:
                item["accidentName"] = tr.xpath(".//a/text()").extract()[0]
            except Exception as e:
                print(e)
            try:
                item["country"] = tr.xpath(".//td[2]/text()").extract()[0]
            except Exception as e:
                print(e)
            try:
                item["province"] = tr.xpath(".//td[3]/text()").extract()[0]
            except Exception as e:
                print(e)
            try:
                item["accidentClass"] = tr.xpath(".//td[4]/text()").extract()[0]
            except Exception as e:
                print(e)
            try:
                item["accidentType"] = tr.xpath(".//td[5]/text()").extract()[0]
            except Exception as e:
                print(e)
            try:
                item["accidentDate"] = tr.xpath(".//td[6]/text()").extract()[0]
            except Exception as e:
                print(e)

            descUrl = """http://accident.nrcc.com.cn:9090/Portalsite/""" + tr.xpath(".//a/@href").extract()[0]
            request = Request(descUrl, callback=self.parseDescription, priority=123)
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
        try:
            pTextList =select.css(".content_text").xpath("//p/text()")
            for pText in pTextList[:-2]:
                try:
                    desc = desc + pText.extract()
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

        try:
            hour = self.hourRe.search(desc)
            if hour:
                item["accidentHour"] = hour.group()
        except Exception as e:
            print(e)
        try:
            noon = self.noonRe.search(desc)
            if noon:
                item["accidentNoon"] = noon.group()
        except Exception as e:
            print(e)

        item["accidentDescription"] = desc
        yield item
        pass

