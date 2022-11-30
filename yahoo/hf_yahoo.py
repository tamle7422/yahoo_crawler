import re
import logging
from datetime import datetime
from scrapy.loader import ItemLoader
from .items import StocksItem
from .switch_month import switchMonthThreeLetters

def getLinks(self,response):
    try:
        # //*[@id="recommendations-by-symbol"]/table/tbody/tr[1]/td[1]/a
        links = checkEmpty(response.xpath( \
            "..//*[@id='recommendations-by-symbol']/table/tbody/tr/td[1]/a[(@title)]/@href").extract())
        if (links != "None"):
            self.name = links
        else:
            self.name = "None"

    except Exception as ex:
        print("exception => error in get links --- {0}".format(ex))
        self.name = "None"

def setName1(self,name):
    try:
        if (name != "None"):
            self.name = name
        else:
            self.name = "None"

    except Exception as ex:
        print("exception --- error in set name1 => {0}".format(ex))
        self.name = "None"

def setName(self,response):
    try:
        # //*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1
        name = checkEmpty(response.xpath( \
            "..//*[@id='quote-header-info']/div[2]/div[1]/div[1]/h1/text()").extract()[0])
        if (name != "None"):
            if (re.search("[\(]+", name) == None):
                self.name = name
            else:
                self.name = name.split("(")[0].strip()
        else:
            self.name = "None"

    except Exception as ex:
        print("exception --- error in set name => {0}".format(ex))
        self.name = "None"

def setSymbol1(self,symbol):
    try:
        if (symbol != "None"):
            self.symbol = symbol
        else:
            self.symbol = "None"

    except Exception as ex:
        print("exception --- error in set symbol1 => {0}".format(ex))
        self.symbol = "None"

def setSymbol(self):
    try:
        if (self.name != "None"):
            if (re.search(r"[\(]+",self.name) != None):
                splitStr = self.name.split("(")[1]
                self.symbol = splitStr.replace(")","")
            else:
                self.symbol = "None"
        else:
            self.symbol = "None"

    except Exception as ex:
        print("exception --- error in set symbol => {0}".format(ex))
        self.symbol = "None"

def setPointChange(self,response):
    try:
        # //*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[2]/span
        pointChange = checkEmpty(response.xpath( \
            "..//*[@id='quote-header-info']/div[3]/div[1]/div[1]/fin-streamer[2]/span/text()").get())
        if (pointChange != "None"):
            self.pointChange = re.sub("[\(\)]+","",pointChange)
        else:
            self.pointChange = "None"

    except Exception as ex:
        print("exception --- error in set point change => {0}".format(ex))
        self.pointChange = "None"

def setPercentChange(self,response):
    try:
        # //*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[3]/span/text()
        percentChange = checkEmpty(response.xpath( \
            "..//*[@id='quote-header-info']/div[3]/div[1]/div/fin-streamer[3]/span/text()").get())
        if (percentChange != "None"):
            self.percentChange = re.sub("[\(\)]+","",percentChange)
        else:
            self.percentChange = "None"

    except Exception as ex:
        print("exception --- error in set percent change => {0}".format(ex))
        self.percentChange = "None"

def setPrice(self,response):
    try:
        # //div[contains(@class,'D(ib)')]/fin-streamer[contains(@class,'Fw(b)')]/text()
        price = checkEmpty(response.xpath( \
            "..//*[@id='quote-header-info']/div[3]/div[1]/div/fin-streamer[1]/text()").get())
        if (price != "None"):
            self.price = price
        else:
            self.price = "None"

    except Exception as ex:
        print("exception --- error in set price => {0}".format(ex))
        self.price = "None"

def setPreviousClosePrice(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]
        previousClosePrice = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[1]/table/tbody/tr[1]/td[2]/text()").get())
        if (previousClosePrice != "None"):
            self.previousClosePrice = previousClosePrice
        else:
            self.previousClosePrice = "None"

    except Exception as ex:
        print("exception --- error in set previous close price => {0}".format(ex))
        self.previousClosePrice = "None"

def setOpenPrice(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]
        openPrice = checkEmpty(
            response.xpath("..//*[@id='quote-summary']/div[1]/table/tbody/tr[2]/td[2]/text()").get())
        if (openPrice != "None"):
            self.openPrice = openPrice
        else:
            self.openPrice = "None"

    except Exception as ex:
        print("exception --- error in set open price => {0}".format(ex))
        self.openPrice = "None"

def setBid(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]
        bid = checkEmpty(
            response.xpath("..//*[@id='quote-summary']/div[1]/table/tbody/tr[3]/td[2]/text()").get())
        if (bid != "None"):
            self.bid = bid
        else:
            self.bid = "None"

    except Exception as ex:
        print("exception --- error in set bid => {0}".format(ex))
        self.bid = "None"

def setAsk(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]
        ask = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[1]/table/tbody/tr[4]/td[2]/text()").get())
        if (ask != "None"):
            self.ask = ask
        else:
            self.ask = "None"

    except Exception as ex:
        print("exception --- error in set ask => {0}".format(ex))
        self.ask = "None"

def setDayRange(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]
        dayRange = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[1]/table/tbody/tr[5]/td[2]/text()").get())
        if (dayRange != "None"):
            self.lowDayRange = dayRange.split("-")[0]
            self.highDayRange = dayRange.split("-")[1]
        else:
            self.lowDayRange = "None"
            self.highDayRange = "None"

    except Exception as ex:
        print("exception --- error in set day range => {0}".format(ex))
        self.lowDayRange = "None"
        self.highDayRange = "None"

def set52WeekRange(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]
        _52WeekRange = checkEmpty(response.xpath(
            "..//*[@id='quote-summary']/div[1]/table/tbody/tr[6]/td[2]/text()").get())
        if (_52WeekRange != "None"):
            self.low52WeekRange = _52WeekRange.split("-")[0].strip()
            self.high52WeekRange = _52WeekRange.split("-")[1].strip()

        else:
            self.low52WeekRange = "None"
            self.high52WeekRange = "None"

    except Exception as ex:
        print("exception --- error in set 52 week range => {0}".format(ex))
        self.low52WeekRange = "None"
        self.high52WeekRange = "None"

def setVolume(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/fin-streamer/span/text()
        volume = checkEmpty(response.xpath(
            "..//*[@id='quote-summary']/div[1]/table/tbody/tr[7]/td[2]/fin-streamer/text()").get())
        if (volume != "None"):
            self.volume = re.sub(r",","",volume)
        else:
            self.volume = "None"

    except Exception as ex:
        print("exception --- error in set volume => {0}".format(ex))
        self.volume = "None"

def setAverageVolume(self,response):
    try:
        # //*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]
        averageVolume = checkEmpty(response.xpath(
            "..//*[@id='quote-summary']/div[1]/table/tbody/tr[8]/td[2]/text()").get())
        if (averageVolume != "None"):
            self.averageVolume = re.sub(r"[\,]+","",averageVolume)
        else:
            self.averageVolume = "None"

    except Exception as ex:
        print("exception --- error in set average volume => {0}".format(ex))
        self.averageVolume = "None"

def setMarketCap(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]
        marketCap = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[2]/table/tbody/tr[1]/td[2]/text()").get())
        if (marketCap != "None"):
            self.marketCap = re.sub(r"[BMbm]+","",marketCap)
        else:
            self.marketCap = "None"

    except Exception as ex:
        print("exception => error in set market cap --- {0}".format(ex))
        self.marketCap = "None"

def setBeta(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]
        beta = checkEmpty( \
            response.xpath("..//*[@id='quote-summary']/div[2]/table/tbody/tr[2]/td[2]/text()").get())
        if (beta != "None"):
            self.beta = beta
        else:
            self.beta = "None"

    except Exception as ex:
        print("exception -- error in set beta => {0}".format(ex))
        self.beta = "None"

def setPriceEarningsRatio(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]
        priceEarningsRatio = checkEmpty(
            response.xpath("..//*[@id='quote-summary']/div[2]/table/tbody/tr[3]/td[2]/text()").get())
        if (priceEarningsRatio != "None"):
            self.priceEarningsRatio = re.sub("[\,]+","",priceEarningsRatio)
        else:
            self.priceEarningsRatio = "None"

    except Exception as ex:
        print("exception --- error in set price earnings ratio => {0}".format(ex))
        self.priceEarningsRatio = "None"

def setEarningsPerShare(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]
        earningsPerShare = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[2]/table/tbody/tr[4]/td[2]/text()").get())
        if (earningsPerShare != "None"):
            self.earningsPerShare = earningsPerShare
        else:
            self.earningsPerShare = "None"

    except Exception as ex:
        print("exception --- error in set earnings per share => {0}".format(ex))
        self.earningsPerShare = "None"

def setEarningsDate(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[5]/td[2]/span[1]
        earningsDate = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[2]/table/tbody/tr[5]/td[@data-test='EARNINGS_DATE-value']/span/text()").extract())
        if (earningsDate != "None"):
            self.earningsDate = earningsDate
        else:
            self.earningsDate = "None"

    except Exception as ex:
        print("exception --- error in set earnings date => {0}".format(ex))
        self.earningsDate = "None"


def setForwardDividendAndYield(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[6]/td[2]
        forwardDividendAndYield = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[2]/table/tbody/tr[6]/td[@data-test='DIVIDEND_AND_YIELD-value']/text()").extract())
        if (forwardDividendAndYield != "None"):
            if (re.search("[\(]+",forwardDividendAndYield[0]) != None):
                splitStr = forwardDividendAndYield[0].split("(")
                self.forwardDividend = splitStr[0].strip()
                self.yieldPercent = re.sub("[\%\)]+","",splitStr[1].strip())
            else:
                self.forwardDividend = "None"
                self.yieldPercent = "None"
        else:
            self.forwardDividend = "None"
            self.yieldPercent = "None"

    except Exception as ex:
        print("exception --- error in set forward dividend and yield => {0}".format(ex))
        self.forwardDividend = "None"
        self.yieldPercent = "None"

def setExDividendDate(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[7]/td[2]/span
        exDividendDate = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[2]/table/tbody/tr[7]/td[@data-test='EX_DIVIDEND_DATE-value']/span/text()").get())
        if (exDividendDate != "None"):
            self.exDividendDate = exDividendDate
        else:
            self.exDividendDate = "None"

    except Exception as ex:
        print("exception --- error in set ex dividend date => {0}".format(ex))
        self.exDividendDate = "None"

def set1YearTarget(self,response):
    try:
        # //*[@id="quote-summary"]/div[2]/table/tbody/tr[8]/td[2]
        _1YearTarget = checkEmpty(response.xpath( \
            "..//*[@id='quote-summary']/div[2]/table/tbody/tr[8]/td[@data-test='ONE_YEAR_TARGET_PRICE-value']/text()").get())
        if (_1YearTarget != "None"):
            self._1YearTarget = _1YearTarget
        else:
            self._1YearTarget = "None"

    except Exception as ex:
        print("exception --- error in set 1 year target => {0}".format(ex))
        self._1YearTarget = "None"

# ----------------------------------------------------------------------------------------------------------------------

def resetStock(self):
    try:
        self.name = ""
        self.symbol = ""
        self.price = ""
        self.previousClosePrice = ""
        self.openPrice = ""
        self.bid = ""
        self.ask = ""
        self.dayRange = ""
        self._52WeekRange = ""
        self.volume = ""
        self.averageVolume = ""
        self.marketCap = ""
        self.beta = ""
        self.priceEarningsRatio = ""
        self.earningsPerShare = ""
        self.forwardDividend = ""
        self.yieldPercent = ""

    except Exception as ex:
        print("exception --- error in reset stock => {0}".format(ex))

def setDate(self,selPath):
    try:
        month = checkEmpty(selPath.xpath(".//td/span/span[@class='month']/text()").get())
        day = checkEmpty(selPath.xpath(".//td/span/span[@class='day']/text()").get())
        year = checkEmpty(selPath.xpath(".//td/span/span[@class='year']/text()").get())

        if (month != "None"):
            monthNum = switchMonthThreeLetters(month)

        if (monthNum != "None" and day != "None" and year != "None"):
            self.date = monthNum + "/" + day + "/" + year
        else:
            self.date = "None"

    except Exception as ex:
        print("exception --- error in set date => {0}".format(ex))
        self.date = "None"

def loadStocksItem(self,response):
    try:
        self.name = self.name if (len(self.name) != 0) else "None"
        self.symbol = self.symbol if (len(self.symbol) != 0) else "None"
        self.price = self.price if (len(self.price) != 0) else "None"
        self.pointChange = self.pointChange if (len(self.pointChange) != 0) else "None"
        self.percentChange = self.percentChange if (len(self.percentChange) != 0) else "None"
        self.previousClosePrice = self.previousClosePrice if (len(self.previousClosePrice) != 0) else "None"
        self.openPrice = self.openPrice if (len(self.openPrice) != 0) else "None"
        self.bid = self.bid if (len(self.bid) != 0) else "None"
        self.ask = self.ask if (len(self.ask) != 0) else "None"
        self.lowDayRange = self.lowDayRange if (len(self.lowDayRange) != 0) else "None"
        self.highDayRange = self.highDayRange if (len(self.highDayRange) != 0) else "None"
        self.low52WeekRange = self.low52WeekRange if (len(self.low52WeekRange) != 0) else "None"
        self.high52WeekRange = self.high52WeekRange if (len(self.high52WeekRange) != 0) else "None"
        self.volume = self.volume if (len(self.volume) != 0) else "None"
        self.averageVolume = self.averageVolume if (len(self.averageVolume) != 0) else "None"
        self.marketCap = self.marketCap if (len(self.marketCap) != 0) else "None"
        self.beta = self.beta if (len(self.beta) != 0) else "None"
        self.priceEarningsRatio = self.priceEarningsRatio if (len(self.priceEarningsRatio) != 0) else "None"
        self.earningsPerShare = self.earningsPerShare if (len(self.earningsPerShare) != 0) else "None"
        self.earningsDate = self.earningsDate if (len(self.earningsDate) != 0) else "None"
        self.forwardDividend = self.forwardDividend if (len(self.forwardDividend) != 0) else "None"
        self.exDividendDate = self.exDividendDate if (len(self.exDividendDate) != 0) else "None"
        self.yieldPercent = self.yieldPercent if (len(self.yieldPercent) != 0) else "None"

        loader = ItemLoader(item=StocksItem(),response=response)
        loader.add_value("name",self.name)
        loader.add_value("symbol",self.symbol)
        loader.add_value("price",self.price)
        loader.add_value("pointChange",self.pointChange)
        loader.add_value("percentChange",self.percentChange)
        loader.add_value("previousClosePrice",self.previousClosePrice)
        loader.add_value("openPrice",self.openPrice)
        loader.add_value("bid",self.bid)
        loader.add_value("ask",self.ask)
        loader.add_value("lowDayRange",self.lowDayRange)
        loader.add_value("highDayRange",self.highDayRange)
        loader.add_value("low52WeekRange", self.low52WeekRange)
        loader.add_value("high52WeekRange", self.high52WeekRange)
        loader.add_value("volume", self.volume)
        loader.add_value("averageVolume", self.averageVolume)
        loader.add_value("marketCap",self.marketCap)
        loader.add_value("beta",self.beta)
        loader.add_value("priceEarningsRatio",self.priceEarningsRatio)
        loader.add_value("earningsPerShare",self.earningsPerShare)
        loader.add_value("earningsDate",self.earningsDate)
        loader.add_value("forwardDividend",self.forwardDividend)
        loader.add_value("exDividendDate",self.exDividendDate)
        loader.add_value("yieldPercent",self.yieldPercent)
        return loader

    except Exception as ex:
        print("exception --- error in load stocks item => {0}".format(ex))

def checkEmpty(data):
    try:
        if (data == None or len(data) == 0):
            return "None"
        else:
            return data

    except Exception as ex:
        print("exception --- error in check data => {0}".format(ex))
        return "None"

def getTime():
    try:
        now = datetime.now()
        currentDate = now.strftime("%m_%d_%y")
        return currentDate

    except Exception as ex:
        print("exception --- error in get time => {0}".format(ex))
        return "None"

