# -*- coding: utf-8 -*-
import scrapy
import pymysql
from twisted.enterprise import adbapi
import os
import shutil
import logging

class DianpingPipeline(object):
    def __init__(self, dbargs):
        self.dbargs = dbargs
        
        self.insertQuestionSql = r"""INSERT INTO `cumt` 
        (`accidentId`,`accidentName`,`country`,`province`,`accidentClass`,`accidentType`,`accidentDate`,`accidentDescription` ) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s);
"""
    
    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool('pymysql', **(self.dbargs))
        
    def close_spider(self, spider):
        self.dbpool.close()
        
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dbargs = dict(
                      host=settings['MYSQL_HOST'],
                      db=settings['MYSQL_DBNAME'],
                      user=settings['MYSQL_USER'],
                      passwd=settings['MYSQL_PASSWD'],
                      port=settings['MYSQL_PORT'],
                      charset='utf8',
                      #cursorclass=MySQLdb.cursors.DictCursor,
                      use_unicode=True,
                      )
        return cls(dbargs)
    
    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insertTmallShopSql, item)
        return item
    
    def insertTmallShopSql(self, cursor, item):
        try:
          cursor.execute(self.insertQuestionSql, (
            item['accidentId'],
            item['accidentName'],
            item['country'],
            item['province'],
            item['accidentClass'],
            item['accidentType'],
            item['accidentDate'],
            item['accidentDescription']
            ))
        except Exception as e:
            print(e)
            print(item)
     