# define your item pipelines here
# don't forget to add your pipeline to the ITEM_PIPELINES setting
# see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os,re
from sys import platform
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from .items import StockItem
from datetime import datetime

class StockPipeline:
    def __init__(self):
        self.stockDir = "csv_files/stock"
        self.stockList = ["company","symbol","currentPrice","previousClosePrice","openPrice","bid","ask", \
            "dayRange","_52WeekRange","volume","averageVolume","marketCap","beta","priceEarningsRatio", \
            "earningsPerShare","forwardDividend","yieldPercent"]

        self.stockWriter = ""
        self.stockFileName = ""
        self.stockExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        # check system; change if on windows
        if (platform != "linux"):
            self.stockDir = "csv_files\\stock"

        today = datetime.today()
        dt = datetime(today.year,today.month,today.day)
        self.stockFileName = "stock_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_"\
            + str(dt.year) + ".csv"

        absolutePathStock = os.path.join(os.getcwd(),self.stockDir)

        self.stockWriter = open(os.path.join(absolutePathStock,self.stockFileName),'wb+')
        self.stockExporter = CsvItemExporter(self.stockWriter)
        self.stockExporter.fields_to_export = self.stockList
        self.stockExporter.start_exporting()

    def spider_closed(self,spider):
        self.stockExporter.finish_exporting()
        self.stockWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,StockItem)):
            if (len(item) == 0):
                return item
            else:
                self.stockExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        if (int(dayOrMonth) <= 9):
            concatStr = "0" + str(dayOrMonth)
            return concatStr
        else:
            return str(dayOrMonth)