import sys
import os,re
import random
import scrapy
import logging
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.log import configure_logging
from ..hf_stocks import checkEmpty,resetFightCard,loadEventItem,checkHeight,setBirthDate,setDate, \
    setEventNameTitleUrl,createUrl,checkFightResult,loadFightCardItem,setFirstRowFightCard,setAge,setHeight, \
    setWeight,setCountry,setLocality,resetFinance,loadFighterItem,setLocation,setAssociation
from ..settings import USER_AGENT_LIST
from scrapy_splash import SplashRequest,SplashFormRequest

class YahooStocksSpider(scrapy.Spider):
    name = 'sherdog_stats'
    allowed_domains = ["finance.yahoo.com","https://finance.yahoo.com/"]
    # start_urls = ['https://www.sherdog.com/events/recent']
    # https://www.sherdog.com/events/recent/267-page

    custom_settings = {
        "ITEM_PIPELINES": {
            'yahoo.pipelines.YahooStocksPipeline': 199,
        },
        "CLOSESPIDER_ITEMCOUNT": 132
    }

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO,filemode="w+"
    )

    def __init__(self,*args,**kwargs):
        super(YahooStocksSpider,self).__init__(*args,**kwargs)
        self.eventUrlList = []
        self.date = ""
        self.eventName = ""
        self.eventTitle = ""
        self.location = ""

        self.fighter1Name = ""
        self.fighter2Name = ""
        self.fighter1Result = ""
        self.fighter2Result = ""
        self.fighterMethodResult = ""

        self.fighterName = ""
        self.birthDate = ""
        self.age = ""
        self.height = ""
        self.weight = ""
        self.fighterClass = ""
        self.win = ""
        self.loss = ""
        self.locality = ""
        self.country = ""

        self.url = "https://www.sherdog.com/events/recent"
        self.script = """
                         function main(splash)
                             local cookies = splash:get_cookies()
                             splash:init_cookies(cookies)

                             assert(splash:go{splash.args.url,headers=splash.args.headers,
                                 http_method=splash.args.http_method,body=splash.args.body})
                             assert(splash:wait(0.5))

                             local entries = splash:history()
                             local last_response = entries[#entries].response
                            
                             return {
                                 url = splash:url(),
                                 headers = last_response.headers,
                                 http_status = last_response.status,
                                 cookies = splash:get_cookies(),
                                 html = splash:html()
                                 -- png = splash:png(),
                                 -- har = splash:har()
                             }
                         end
                     """
        self.script2 = """
                          function main(splash,args)
                              local cookies = splash:get_cookies()
                              splash:init_cookies(cookies)
                              assert(splash:go(splash.args.url))
                              assert(splash:wait(1.5))

                              return {
                                  cookies,
                                  html = splash:html(),
                                  -- png = splash:png(),
                                  -- har = splash:har()
                              }
                          end
                      """

    def start_requests(self):
        yield SplashRequest(url=self.url,callback=self.parseFirstEvent,\
            endpoint="execute",args={"lua_source": self.script2},
            headers={"User-Agent": random.choice(USER_AGENT_LIST)})

    def parseFirstEvent(self,response):
        try:
            # splash renders with body tag
            trTag = checkEmpty(response.xpath("//table[@class='event']/tbody/tr[contains(@class,'odd') or contains(@class,'even')]"))
            if (trTag != "None"):
                for i in trTag:
                    setDate(self,i)
                    setEventNameTitleUrl(self,i,response)

                    location = checkEmpty(i.xpath(".//td[4]/span/text()").get())
                    if (location != "None"):
                        setLocation(self,location)
                    else:
                        self.location = "None"

                    loader = loadEventItem(self,response)
                    yield loader.load_item()
                    yield SplashRequest(url=self.eventUrl,callback=self.parseFightCard,\
                        endpoint="execute",args={"lua_source": self.script2},\
                        headers={"User-Agent": random.choice(USER_AGENT_LIST)})

            createUrl(self)
            for aUrl in self.eventUrlList:
                yield SplashRequest(url=aUrl,callback=self.parseEvent,\
                    endpoint="execute",args={"lua_source": self.script2}, \
                    headers={"User-Agent": random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            logging.info("error => {0}".format(ex))
            print("error => %s" % ex)

    def parseEvent(self,response):
        try:
            trTag = checkEmpty(response.xpath("//table[@class='event']/tbody/tr[contains(@class,'odd') or contains(@class,'even')]"))
            if (trTag != "None"):
                for i in trTag:
                    setDate(self,i)
                    setEventNameTitleUrl(self,i,response)

                    location = checkEmpty(i.xpath(".//td[4]/span/text()").get())
                    if (location != "None"):
                        setLocation(self,location)
                    else:
                        self.location = "None"

                    loader = loadEventItem(self,response)
                    yield loader.load_item()

        except Exception as ex:
            print("exception: {y}".format(y=ex))

    def parseFightCard(self,response):
        try:
            resetFightCard(self)
            setFirstRowFightCard(self,response)
            loader = loadFightCardItem(self,response)
            yield loader.load_item()

            trTag = checkEmpty(response.xpath("//div[@class='content table']/table/tbody/tr[contains(@class,'even') or contains(@class,'odd')]"))
            if (trTag != "None"):
                for i in trTag:
                    resetFightCard(self)
                    fighter1Name = checkEmpty(i.xpath(".//td[@class='text_right col_fc_upcoming']/div[@class='fighter_result_data']/a/span/text()").get())
                    if (fighter1Name != "None"):
                        self.fighter1Name = fighter1Name.lower()
                    else:
                        self.fighter1Name = "None"

                    fighter1Url = checkEmpty(i.xpath(".//td[@class='text_right col_fc_upcoming']/div[@class='fighter_result_data']/a/@href").get())
                    if (fighter1Url != "None"):
                        self.fighter1Url = response.urljoin(fighter1Url)
                        yield SplashRequest(url=self.fighter1Url,callback=self.parseFighterStats,\
                            endpoint="execute",args={"lua_source": self.script2},\
                            headers={"User-Agent": random.choice(USER_AGENT_LIST)})

                    else:
                        self.fighter1Url = "None"

                    fighter1Result = checkEmpty(i.xpath(".//td[@class='text_right col_fc_upcoming']/div[@class='fighter_result_data']/span/text()").get())
                    if (fighter1Result != "None"):
                        self.fighter1Result = checkFightResult(self,fighter1Result.lower())
                    else:
                        self.fighter1Result = "None"

                    fighter2Name = checkEmpty(i.xpath(".//td[@class='text_left col_fc_upcoming']/div[@class='fighter_result_data']/a/span/text()").get())
                    if (fighter2Name != "None"):
                        self.fighter2Name = fighter2Name.lower()
                    else:
                        self.fighter2Name = "None"

                    fighter2Url = checkEmpty(i.xpath(".//td[@class='text_left col_fc_upcoming']/div[@class='fighter_result_data']/a/@href").get())
                    if (fighter2Url != "None"):
                        self.fighter2Url = response.urljoin(fighter2Url)
                        yield SplashRequest(url=self.fighter2Url,callback=self.parseFighterStats,\
                            endpoint="execute",args={"lua_source": self.script2},\
                            headers={"User-Agent": random.choice(USER_AGENT_LIST)})

                    else:
                        self.fighter2Url = "None"

                    fighter2Result = checkEmpty(i.xpath(".//td[@class='text_left col_fc_upcoming']/div[@class='fighter_result_data']/span/text()").get())
                    if (fighter2Result != "None"):
                        self.fighter2Result = checkFightResult(self,fighter2Result.lower())
                    else:
                        self.fighter2Result = "None"

                    fighterMethodResult = checkEmpty(i.xpath(".//td[5]/text()").get())
                    if (fighterMethodResult != "None"):
                        self.fighterMethodResult = fighterMethodResult.lower()
                    else:
                        self.fighterMethodResult

                    loader = loadFightCardItem(self,response)
                    yield loader.load_item()

        except Exception as ex:
            print("exception: %s" % ex)

    def parseFighterStats(self,response):
        try:
            resetFighterStats(self)

            fighterName = checkEmpty(response.xpath("//div[@class='module bio_fighter vcard']/h1/span/text()").get())
            if (fighterName != "None"):
                self.fighterName = fighterName.lower()
            else:
                self.fighterName = "None"

            birthDate = checkEmpty(response.xpath("//div[@class='birth_info']/span/span/text()").get())
            if (birthDate != "None"):
                setBirthDate(self,birthDate)
            else:
                self.birthDate = "None"

            age = checkEmpty(response.xpath("//div[@class='birth_info']/span/strong/text()").get())
            if (age != "None"):
                setAge(self,age)
            else:
                self.age = "None"

            height = checkEmpty(response.xpath("//div[@class='size_info']/span[@class='item height']/strong/text()").get())
            if (height != "None"):
                setHeight(self,height)
            else:
                self.height = "None"

            weight = checkEmpty(response.xpath("//div[@class='size_info']/span[@class='item weight']/strong/text()").get())
            if (weight != "None"):
                setWeight(self,weight)
            else:
                self.weight = "None"

            fighterClass = checkEmpty(response.xpath("//div[@class ='size_info']/h6/strong/a/text()").get())
            if (fighterClass != "None"):
                self.fighterClass = fighterClass
            else:
                self.fighterClass = ""

            win = checkEmpty(response.xpath("//div[@class='bio_graph']/span[@class='card']/span[2]/text()").get())
            if (win != "None"):
                self.win = win
            else:
                self.win = ""

            loss = checkEmpty(response.xpath("//div[@class='bio_graph loser']/span[@class='card']/span[2]/text()").get())
            if (loss != "None"):
                self.loss = loss
            else:
                self.loss = ""

            locality = checkEmpty(response.xpath("//div[@class='birth_info']/span[@class='item birthplace']/span/span[@class='locality']/text()").get())
            if (locality != "None"):
                setLocality(self,locality)
            else:
                self.locality = "None"

            country = checkEmpty(response.xpath("//div[@class='birth_info']/span[@class='item birthplace']/strong[@itemprop='nationality']/text()").get())
            if (country != "None"):
                setCountry(self,country)
            else:
                self.country = "None"

            loader = loadFighterItem(self,response)
            yield loader.load_item()

        except Exception as ex:
            print("exception: {x}".format(x=ex))

class SherdogFighterSpider(CrawlSpider):
    name = "sherdog_fighter"
    allowed_domains = ["www.sherdog.com","sherdog.com"]
    start_urls = ["https://www.sherdog.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'sherdog.pipelines.SherdogFighterPipeline': 275,
        },
        "CLOSESPIDER_ITEMCOUNT": 159
    }
    handle_httpstatus_list = [403]

    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='log.txt',format='%(levelname)s: %(message)s', \
        level=logging.INFO,filemode="w+"
    )

    rules = (
        # extract links matching fighter and parse with spider's method
        Rule(LinkExtractor(allow=('fighter/'),deny=()),
             process_request="parseFromRule"),
    )

    def __init__(self,*args,**kwargs):
        super(SherdogFighterSpider,self).__init__(*args,**kwargs)
        self.fighterName = ""
        self.birthDate = ""
        self.age = ""
        self.height = ""
        self.weight = ""
        self.association = ""
        self.fighterClass = ""
        self.win = ""
        self.loss = ""
        self.locality = ""
        self.country = ""

        self.count = 0
        # self.url = "https://www.sherdog.com"
        self.script = """
                         function main(splash,args)
                             local cookies = splash:get_cookies()
                             splash:init_cookies(cookies)
                             assert(splash:go(splash.args.url))
                             assert(splash:wait(1.5))

                             return {
                                 cookies,
                                 html = splash:html(),
                                 -- png = splash:png(),
                                 -- har = splash:har()
                             }
                         end
                      """

    def parseFromRule(self,request,htmlResponse):
        # error: spider must return request, item, or None, got 'generator'
        # return instead of yield generator
        return SplashRequest(url=request.url,callback=self.parseFighter,
            endpoint="execute",args={"lua_source": self.script},
            headers={"User-Agent": random.choice(USER_AGENT_LIST)})

    def parseFighter(self,response):
        try:
            print("here...")
            resetFighterStats(self)
            # //div[@class ='birth_info']/span/span/text()

            fighterName = checkEmpty(response.xpath("//div[@class='module bio_fighter vcard']/h1/span/text()").get())
            if (fighterName != "None"):
                self.fighterName = fighterName.lower()
            else:
                self.fighterName = "None"

            birthDate = checkEmpty(response.xpath("//div[@class='birth_info']/span/span/text()").get())
            if (birthDate != "None"):
                setBirthDate(self, birthDate)
            else:
                self.birthDate = "None"

            age = checkEmpty(response.xpath("//div[@class='birth_info']/span/strong/text()").get())
            if (age != "None"):
                setAge(self, age)
            else:
                self.age = "None"

            height = checkEmpty(response.xpath("//div[@class='size_info']/span[@class='item height']/strong/text()").get())
            if (height != "None"):
                setHeight(self, height)
            else:
                self.height = "None"

            weight = checkEmpty(response.xpath("//div[@class='size_info']/span[@class='item weight']/strong/text()").get())
            if (weight != "None"):
                setWeight(self,weight)
            else:
                self.weight = "None"

            association = checkEmpty(response.xpath("//h5/strong/span/a/span/text()").get())
            if (association != "None"):
                setAssociation(self,association)
            else:
                self.association = ""

            fighterClass = checkEmpty(response.xpath("//div[@class ='size_info']/h6/strong/a/text()").get())
            if (fighterClass != "None"):
                self.fighterClass = str(fighterClass).lower()
            else:
                self.fighterClass = ""

            win = checkEmpty(response.xpath("//div[@class='bio_graph']/span[@class='card']/span[2]/text()").get())
            if (win != "None"):
                self.win = win
            else:
                self.win = ""

            loss = checkEmpty(response.xpath("//div[@class='bio_graph loser']/span[@class='card']/span[2]/text()").get())
            if (loss != "None"):
                self.loss = loss
            else:
                self.loss = ""

            locality = checkEmpty(response.xpath(
                "//div[@class='birth_info']/span[@class='item birthplace']/span/span[@class='locality']/text()").get())
            if (locality != "None"):
                setLocality(self, locality)
            else:
                self.locality = "None"

            country = checkEmpty(response.xpath("//div[@class='birth_info']/span[@class='item birthplace']/strong[@itemprop='nationality']/text()").get())
            if (country != "None"):
                setCountry(self, country)
            else:
                self.country = "None"

            loader = loadFighterItem(self, response)
            yield loader.load_item()

        except Exception as ex:
            print("error => %s" % ex)
            logging.info("error => {0}".format(ex))





