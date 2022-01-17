import re
from scrapy.loader import ItemLoader
from .items import FinanceItem
import logging
from .switch_month import switchMonthThreeLetters

def resetFinance(self):
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

def setLocality(self,locality):
    if (re.search(r"N/A",locality) != None):
        self.locality = "None"
    else:
        subComma = re.sub(r"[\,]",";",locality)
        self.locality = '"' + subComma + '"'

def setCountry(self,country):
    if (re.search(r"N/A",country) != None):
        self.country = "None"
    else:
        self.country = country

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

def setEventNameTitleUrl(self,selPath,response):
    eventName = checkEmpty(selPath.xpath(".//td[2]/a/text()").get())
    if (eventName != "None"):
        self.eventName = eventName
    else:
        self.eventName = "None"

    eventTitle = checkEmpty(selPath.xpath(".//td[3]/a/text()").get())
    if (eventTitle != "None"):
        self.eventTitle = eventTitle
    else:
        self.eventTitle = "None"

    eventUrl = checkEmpty(selPath.xpath(".//td[2]/a/@href").get())
    if (eventUrl != "None"):
        urlJoin = checkEmpty(response.urljoin(eventUrl))
        if (urlJoin != "None"):
            self.eventUrl = urlJoin
        elif (urlJoin == "None"):
            self.eventUrl = "None"

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

def loadEventItem(self,response):
    self.date = self.date if (self.date != "") else "None"
    self.eventName = self.eventName if (self.eventName != "") else "None"
    self.eventTitle = self.eventTitle if (self.eventTitle != "") else "None"
    self.location = self.location if (self.location != "") else "None"

    loader = ItemLoader(item=EventItem(),response=response)
    loader.add_value("date",self.date)
    loader.add_value("eventName",self.eventName)
    loader.add_value("eventTitle",self.eventTitle)
    loader.add_value("location",self.location)
    return loader

def loadFightCardItem(self,response):
    self.fighter1Name = self.fighter1Name if (self.fighter1Name != "") else "None"
    self.fighter2Name = self.fighter2Name if (self.fighter2Name != "") else "None"
    self.fighter1Result = self.fighter1Result if (self.fighter1Result != "") else "None"
    self.fighter2Result = self.fighter2Result if (self.fighter2Result != "") else "None"
    self.fighterMethodResult = self.fighterMethodResult if (self.fighterMethodResult != "") else "None"

    loader = ItemLoader(item=FightCardItem(),response=response)
    loader.add_value("fighter1Name",self.fighter1Name)
    loader.add_value("fighter2Name",self.fighter2Name)
    loader.add_value("fighter1Result",self.fighter1Result)
    loader.add_value("fighter2Result",self.fighter2Result)
    loader.add_value("fighterMethodResult",self.fighterMethodResult)
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