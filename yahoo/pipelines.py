# define your item pipelines here
# don't forget to add your pipeline to the ITEM_PIPELINES setting
# see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os,re
from sys import platform
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from .items import FinanceItem
from datetime import datetime

class YahooStocksPipeline:
    def __init__(self):
        self.outputFinanceDir = "yahoo/csv_files/finance"
        self.financeList = ["fighter1Name","fighter1Result","fighter2Name","fighter2Result", \
            "fighterMethodResult"]

        self.financeWriter = ""
        self.financeFileName = ""
        self.financeExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        # check system; change if on windows
        if (platform != "linux"):
            self.outputFinanceDir = "csv_files\\finance"

        today = datetime.today()
        dt = datetime(today.year,today.month,today.day)
        self.specificEventFileName = "yahoo_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_"\
            + str(dt.year) + "_.csv"

        absolutePathSpecificEvent = os.path.join(os.getcwd(),self.outputSpecificEventDir)
        self.specificEventWriter = open(os.path.join(absolutePathSpecificEvent,self.specificEventFileName),'wb+')
        self.specificEventExporter = CsvItemExporter(self.specificEventWriter)
        self.specificEventExporter.fields_to_export = self.specificEventList
        self.specificEventExporter.start_exporting()

    def spider_closed(self,spider):
        self.specificEventExporter.finish_exporting()
        self.specificEventWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,FinanceItem)):
            if (len(item) == 0):
                return item
            else:
                self.specificEventExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        if (int(dayOrMonth) <= 9):
            concatStr = "0" + str(dayOrMonth)
            return concatStr
        else:
            return str(dayOrMonth)