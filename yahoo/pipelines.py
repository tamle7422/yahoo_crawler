'''
Define your item pipelines here

don't forget to add your pipeline to the ITEM_PIPELINES setting
see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html






****                 ****

'''
import os,re
from sys import platform
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from .items import StocksItem
from datetime import datetime

class YahooStocksPipeline:
    def __init__(self):
        self.stocksDir = "csv_files/stocks"
        self.stocksList = ["name","symbol","price","pointChange","percentChange","previousClosePrice","openPrice","bid","ask", \
            "lowDayRange","highDayRange","low52WeekRange","high52WeekRange","volume","averageVolume","marketCap","beta", \
            "priceEarningsRatio","earningsPerShare","earningsDate,","forwardDividend","exDividendDate","yieldPercent"]

        self.stocksWriter = ""
        self.stocksFileName = ""
        self.stocksExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        try:
            # check system; change if on windows
            if (platform != "linux"):
                self.stocksDir = "csv_files\\stocks"

            today = datetime.today()
            dt = datetime(today.year,today.month,today.day)

            self.stocksFileName = "yahoo_stocks_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(
                dt.day) + "_" + str(dt.year) + ".csv"

            absolutePathStocks = os.path.join(os.getcwd(),self.stocksDir)

            self.stocksWriter = open(os.path.join(absolutePathStocks,self.stocksFileName),'wb+')
            self.stocksExporter = CsvItemExporter(self.stocksWriter)
            self.stocksExporter.fields_to_export = self.stocksList
            self.stocksExporter.start_exporting()

        except Exception as ex:
            print("exception --- error in spider opened => {0}".format(ex))

    def spider_closed(self,spider):
        self.stocksExporter.finish_exporting()
        self.stocksWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,StocksItem)):
            if (len(item) == 0):
                return item
            else:
                self.stocksExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        try:
            if (int(dayOrMonth) <= 9):
                concatStr = "0" + str(dayOrMonth)
                return concatStr
            else:
                return str(dayOrMonth)

        except Exception as ex:
            print("exception --- error in check month day => {0}".format(ex))

class YahooStocksRulePipeline:
    def __init__(self):
        self.stocksDir = "./csv_files/stocks"
        self.stocksList = ["name","symbol","price","pointChange","percentChange","previousClosePrice","openPrice","bid","ask", \
            "lowDayRange","highDayRange","low52WeekRange","high52WeekRange","volume","averageVolume","marketCap","beta", \
            "priceEarningsRatio","earningsPerShare","earningsDate,","forwardDividend","exDividendDate","yieldPercent"]

        self.stocksWriter = ""
        self.stocksFileName = ""
        self.stocksExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        # check system; change if on windows
        if (platform != "linux"):
            self.stocksDir = "csv_files\\stocks"

        nowDate = datetime.today()
        dt = datetime(nowDate.year,nowDate.month,nowDate.day)
        self.stocksFileName = "yahoo_stocks_rule_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_" \
            + str(dt.year) + ".csv"

        absolutePathStocks = os.path.join(os.getcwd(),self.stocksDir)
        self.stocksWriter = open(os.path.join(absolutePathStocks,self.stocksFileName),'wb+')
        self.stocksExporter = CsvItemExporter(self.stocksWriter)
        self.stocksExporter.fields_to_export = self.stocksList
        self.stocksExporter.start_exporting()

    def spider_closed(self,spider):
        self.stocksExporter.finish_exporting()
        self.stocksWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,StocksItem)):
            if (len(item) == 0):
                return item
            else:
                self.stocksExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        try:
            if (int(dayOrMonth) <= 9):
                concatStr = "0" + str(dayOrMonth)
                return concatStr
            else:
                return str(dayOrMonth)

        except Exception as ex:
            print("exception --- error in check month day => {0}".format(ex))