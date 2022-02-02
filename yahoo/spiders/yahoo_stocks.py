import sys
import os,re
import random
import scrapy
import logging
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.log import configure_logging
from ..hf_yahoo import checkEmpty,resetFightCard,loadEventItem,checkHeight,setBirthDate,setDate, \
    setEventNameTitleUrl,createUrl,checkFightResult,loadFightCardItem,setFirstRowFightCard,setAge,setHeight, \
    setWeight,setVolume,setAverageVolume,resetFinance,loadFighterItem,setLocation,setAssociation
from ..settings import USER_AGENT_LIST
from scrapy_splash import SplashRequest,SplashFormRequest

class YahooStocksSpider(scrapy.Spider):
    name = "yahoo_crawler"
    allowed_domains = ["finance.yahoo.com","https://finance.yahoo.com/"]
    # start_urls = ['https://www.sherdog.com/events/recent']
    # https://www.sherdog.com/events/recent/267-page

    custom_settings = {
        "ITEM_PIPELINES": {
            'yahoo.pipelines.YahooStocksPipeline': 199,
        },
        "CLOSESPIDER_ITEMCOUNT": 44
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO,filemode="w+"
    # )

    def __init__(self,*args,**kwargs):
        super(YahooStocksSpider,self).__init__(*args,**kwargs)
        self.symbol = ""
        self.company = ""
        self.currentPrice = ""
        self.previousClosePrice = ""
        self.openPrice = ""
        self.bid = ""
        self.ask = ""
        self.dayRange = ""
        self._52WeekRange = ""
        self.volume = ""
        self.averageVolume = ""

        self.textFileDir = "text_files"

        self.url = "https://finance.yahoo.com"
        self.urlList = []

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
        try:
            print(os.getcwd())
            fileReader = open(os.path.join(self.textFileDir,"NYSE.txt"),"r")
            next(fileReader)
            companyList = fileReader.readlines()

            for i in companyList:
                combineStr = ""
                splitStr = i.split("\t")
                self.symbol = checkEmpty(splitStr[0].strip())
                self.company = splitStr[1].strip()

                if (self.symbol != "None"):
                    self.url = "https://finance.yahoo.com/quote/" + self.symbol
                    yield SplashRequest(url=self.url, callback=self.parseYahoo, \
                        endpoint="execute", args={"lua_source": self.script2}, \
                        headers={"User-Agent": random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            print("exception => error opening text file for reading --- {0}".format(ex))

    def parseYahoo(self,response):
        try:
            # splash renders with body tag
            self.urlList.append(response.url)

            currentPrice = checkEmpty(response.xpath("//div[contains(@class,'D(ib)')]/fin-streamer[contains(@class,'Fw(b)')]/text()").get())
            if (currentPrice != "None"):
                self.currentPrice = currentPrice
            else:
                self.currentPrice = "None"

            previousClosePrice = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'PREV_CLOSE-value')]/text()").get())
            if (previousClosePrice != "None"):
                self.previousClosePrice = previousClosePrice
            else:
                self.previousClosePrice = "None"

            openPrice = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'OPEN-value')]/text()").get())
            if (openPrice != "None"):
                self.openPrice = openPrice
            else:
                self.openPrice = "None"

            bid = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'BID-value')]/text()").get())
            if (bid != "None"):
                self.bid = bid
            else:
                self.bid = "None"

            ask = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'ASK-value')]/text()").get())
            if (ask != "None"):
                self.ask = ask
            else:
                self.ask = "None"

            dayRange = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'DAYS_RANGE-value')]/text()").get())
            if (dayRange != "None"):
                self.dayRange = dayRange
            else:
                self.dayRange = "None"

            _52WeekRange = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'FIFTY_TWO_WK_RANGE-value')]/text()").get())
            if (_52WeekRange != "None"):
                self._52WeekRange = _52WeekRange
            else:
                self._52WeekRange = "None"

            volume = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'TD_VOLUME-value')]/fin-streamer/text()").get())
            if (volume != "None"):
                setVolume(self,volume)
            else:
                self.volume = "None"

            averageVolume = checkEmpty(response.xpath("//tr[contains(@class,'Bxz(bb)')]/td[contains(@data-test,'AVERAGE_VOLUME_3MONTH-value')]/text()").get())
            if (averageVolume != "None"):
                setAverageVolume(self,averageVolume)
            else:
                self.averageVolume = "None"




            print("")

            print("")




            # loader = loadEventItem(self,response)
            # yield loader.load_item()
            # yield SplashRequest(url=self.eventUrl,callback=self.parseFightCard,\
            #     endpoint="execute",args={"lua_source": self.script2},\
            #     headers={"User-Agent": random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            print("exception => error in parse yahoo --- {0}".format(ex))



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

