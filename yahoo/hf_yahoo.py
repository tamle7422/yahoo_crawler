import re
import logging
from datetime import datetime
from scrapy.loader import ItemLoader
from .items import StockItem
from .switch_month import switchMonthThreeLetters

def getTime():
    now = datetime.now()
    currentDate = now.strftime("%m_%d_%y")
    return currentDate

def resetStock(self):
    self.birthDate = ""
    self.age = ""
    self.height = ""
    self.weight = ""
    self.win = ""
    self.loss = ""
    self.locality = ""
    self.country = ""

def setLocation(self,location):
    subComma = re.sub(r"[\,]",";",location)
    self.location = '"' + subComma + '"'

def setVolume(self,volume):
    try:
        if (volume != "None"):
            self.volume = re.sub(r",","",volume)
        else:
            self.volume = "None"

    except Exception as ex:
        print("exception => error setting volume --- {0}".format(ex))
        self.volume = "None"

def setCompany(self,company):
    try:
        if (company != "None"):
            self.company = company.lower()
        else:
            self.company = "None"

    except Exception as ex:
        print("exception => error setting company --- {0}".format(ex))
        self.company = "None"

def setSymbol(self,symbol):
    try:
        if (symbol != "None"):
            self.symbol = symbol
        else:
            self.symbol = "None"

    except Exception as ex:
        print("exception => error setting symbol --- {0}".format(ex))
        self.symbol = "None"

def setAverageVolume(self,averageVolume):
    try:
        if (averageVolume != "None"):
            self.averageVolume = re.sub(r",","",averageVolume)
        else:
            self.averageVolume = "None"

    except Exception as ex:
        print("exception => error setting average volume --- {0}".format(ex))
        self.averageVolume = "None"

def setMarketCap(self,marketCap):
    try:
        self.marketCap = re.sub(r"B","",marketCap)

    except Exception as ex:
        print("exception => error setting market capitalization --- {0}".format(ex))
        self.marketCap = "None"

def setForwardDividendYield(self,forwardDividendYield):
    try:
        if (forwardDividendYield != "None"):
            splitOpenParen = forwardDividendYield.split("(")
            self.forwardDividend = splitOpenParen[0]
            self.yieldPercent = re.sub(r"[^0-9\.]","",splitOpenParen[1])
        else:
            self.forwardDividend = "None"
            self.yieldPercent = "None"

    except Exception as ex:
        print("exception => error setting forward dividend and yield --- {0}".format(ex))
        self.forwardDividend = "None"
        self.yieldPercent = "None"


def setHeight(self,height):
    if (re.search(r"N/A",height) == None and re.search(r"0'0",height) == None):
        subDoubleQuote = re.sub(r"[\"]","",height)
        splitSingleQuote = subDoubleQuote.split("'")
        self.height = str((int(splitSingleQuote[0]) * 12) + int(splitSingleQuote[1]))
    else:
        self.height = "None"

def setWeight(self,weight):
    subLetters = re.sub(r"[^0-9]","",weight)
    if (subLetters != "0"):
        self.weight = subLetters
    else:
        self.weight = "None"

def setAge(self,age):
    subStr = ""
    if (re.search(r"N/A",age) != None):
        self.age = "None"
    else:
        subStr = re.sub(r"AGE:","",age)
        self.age = subStr.strip()

def setBirthDate(self,birthDate):
    month = ""
    day = ""
    year = ""
    if (re.search(r"N/A",birthDate) != None):
        self.birthDate = "None"
    else:
        splitDash = birthDate.split("-")
        month = splitDash[1]
        day  = splitDash[2]
        year = splitDash[0]

        self.birthDate = month + "/" + day + "/" + year

def setAssociation(self,association):
    self.association = str(association).lower()

def setFirstRowFightCard(self,response):
    try:
        fighter1Name = checkEmpty(response.xpath("//div[@class='fighter left_side']/h3/a/span/text()").get())
        if (fighter1Name != "None"):
            self.fighter1Name = fighter1Name.lower()
        else:
            self.fighter1Name = "None"

        fighter1Result = checkEmpty(response.xpath("//div[@class='fighter left_side']/span[1]/text()").get())
        if (fighter1Result != "None"):
            self.fighter1Result = checkFightResult(self,fighter1Result.lower())
        else:
            self.fighter1Result = "None"

        fighter2Name = checkEmpty(response.xpath("//div[@class='fighter right_side']/h3/a/span/text()").get())
        if (fighter2Name != "None"):
            self.fighter2Name = fighter2Name.lower()
        else:
            self.fighter2Name = "None"

        fighter2Result = checkEmpty(response.xpath("//div[@class='fighter right_side']/span[1]/text()").get())
        if (fighter2Result != "None"):
            self.fighter2Result = checkFightResult(self,fighter2Result.lower())
        else:
            self.fighter2Result = "None"

        fighterMethodResult = checkEmpty(response.xpath("//div[@class='footer']/table/tbody/tr/td[2]/text()").get())
        if (fighterMethodResult != "None"):
            self.fighterMethodResult = fighterMethodResult.lower()
        else:
            self.fighterMethodResult

    except Exception as ex:
        print("exception: {0}".format(ex))

def checkFightResult(self,fightResult):
    if (fightResult == "win"):
        return "W"
    elif (fightResult == "loss"):
        return "L"

def createUrl(self):
    # 1-202
    for i,x in enumerate(range(2,38,2)):
        url = "https://www.sherdog.com/events/recent/{0}-page".format(x)
        self.eventUrlList.append(url)

def setDate(self,selPath):
    month = checkEmpty(selPath.xpath(".//td/span/span[@class='month']/text()").get())
    day = checkEmpty(selPath.xpath(".//td/span/span[@class='day']/text()").get())
    year = checkEmpty(selPath.xpath(".//td/span/span[@class='year']/text()").get())

    if (month != "None"):
        monthNum = switchMonthThreeLetters(month)

    if (monthNum != "None" and day != "None" and year != "None"):
        self.date = monthNum + "/" + day + "/" + year
    else:
        self.date = "None"

def loadStockItem(self,response):
    self.company = self.company if (len(self.company) != 0) else "None"
    self.symbol = self.symbol if (len(self.symbol) != 0) else "None"
    self.currentPrice = self.currentPrice if (len(self.currentPrice) != 0) else "None"
    self.previousClosePrice = self.previousClosePrice if (len(self.previousClosePrice) != 0) else "None"
    self.openPrice = self.openPrice if (len(self.openPrice) != 0) else "None"
    self.bid = self.bid if (len(self.bid) != 0) else "None"
    self.ask = self.ask if (len(self.ask) != 0) else "None"
    self.dayRange = self.dayRange if (len(self.dayRange) != 0) else "None"
    self._52WeekRange = self._52WeekRange if (len(self._52WeekRange) != 0) else "None"
    self.volume = self.volume if (len(self.volume) != 0) else "None"
    self.averageVolume = self.averageVolume if (len(self.averageVolume) != 0) else "None"
    self.marketCap = self.marketCap if (len(self.marketCap) != 0) else "None"
    self.beta = self.beta if (len(self.beta) != 0) else "None"
    self.priceEarningsRatio = self.priceEarningsRatio if (len(self.priceEarningsRatio) != 0) else "None"
    self.earningsPerShare = self.earningsPerShare if (len(self.earningsPerShare) != 0) else "None"
    self.forwardDividend = self.forwardDividend if (len(self.forwardDividend) != 0) else "None"
    self.yieldPercent = self.yieldPercent if (len(self.yieldPercent) != 0) else "None"

    loader = ItemLoader(item=StockItem(),response=response)
    loader.add_value("company", self.company)
    loader.add_value("symbol", self.symbol)
    loader.add_value("currentPrice",self.currentPrice)
    loader.add_value("previousClosePrice",self.previousClosePrice)
    loader.add_value("currentPrice",self.currentPrice)
    loader.add_value("previousClosePrice",self.previousClosePrice)
    loader.add_value("openPrice",self.openPrice)
    loader.add_value("bid",self.bid)
    loader.add_value("ask",self.ask)
    loader.add_value("dayRange",self.dayRange)
    loader.add_value("_52WeekRange",self._52WeekRange)
    loader.add_value("volume",self.volume)
    loader.add_value("averageVolume",self.averageVolume)
    loader.add_value("marketCap",self.marketCap)
    loader.add_value("beta",self.beta)
    loader.add_value("priceEarningsRatio",self.priceEarningsRatio)
    loader.add_value("earningsPerShare",self.earningsPerShare)
    loader.add_value("forwardDividend",self.forwardDividend)
    loader.add_value("yieldPercent",self.yieldPercent)
    return loader

def loadFighterItem(self,response):
    self.fighterName = self.fighterName if (self.fighterName != "") else "None"
    self.birthDate = self.birthDate if (self.birthDate != "") else "None"
    self.age = self.age if (self.age != "") else "None"
    self.height = self.height if (self.height != "") else "None"
    self.weight = self.weight if (self.weight != "") else "None"
    self.association = self.association if (self.association != "") else "None"
    self.fighterClass = self.fighterClass if (self.fighterClass != "") else "None"
    self.win = self.win if (self.win != "") else "None"
    self.loss = self.loss if (self.loss != "") else "None"
    self.locality = self.locality if (self.locality != "") else "None"
    self.country = self.country if (self.country != "") else "None"

    loader = ItemLoader(item=FighterItem(),response=response)
    loader.add_value("fighterName",self.fighterName)
    loader.add_value("birthDate",self.birthDate)
    loader.add_value("age",self.age)
    loader.add_value("height",self.height)
    loader.add_value("weight",self.weight)
    loader.add_value("association",self.association)
    loader.add_value("fighterClass",self.fighterClass)
    loader.add_value("win",self.win)
    loader.add_value("loss",self.loss)
    loader.add_value("locality",self.locality)
    loader.add_value("country",self.country)
    return loader

def resetFightCard(self):
    self.fighter1Name = ""
    self.fighter2Name = ""
    self.fighter1Result = ""
    self.fighter2Result = ""
    self.fighterMethodResult = ""

def checkHeight(data):
    subDoubleQuote = re.sub(r"[\"\\]",'',data)
    if (subDoubleQuote == "0'0" or subDoubleQuote == None):
        subDoubleQuote = "None"
        return subDoubleQuote
    else:
        splitSingleQuote = subDoubleQuote.split("'")
        convInches = (int(splitSingleQuote[0])) * 12 + int(splitSingleQuote[1])
        return str(convInches)

def checkEmpty(data):
    if (data == None):
        data = "None"
        return data
    else:
        return data