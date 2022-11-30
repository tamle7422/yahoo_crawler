import sys
import os,re
import random
import scrapy
import logging
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.log import configure_logging
from ..hf_yahoo import setName1,setSymbol1,setPrice,setPointChange,setPercentChange,setPreviousClosePrice,setOpenPrice, \
    setBid,setDayRange,setMarketCap,set52WeekRange,setVolume,setAverageVolume,setBeta,setPriceEarningsRatio, \
    setEarningsPerShare,setEarningsDate,setForwardDividendAndYield,setExDividendDate, \
    set1YearTarget,checkEmpty,setDate,loadStocksItem,resetStock
from ..settings import USER_AGENT_LIST
from scrapy_splash import SplashRequest,SplashFormRequest

class YahooStocksSpider(scrapy.Spider):
    name = "yahoo_stocks"
    allowed_domains = ["yahoo.com"]
    # start_urls = ['https://www.sherdog.com/events/recent']
    # https://www.sherdog.com/events/recent/267-page

    custom_settings = {
        "ITEM_PIPELINES": {
            'yahoo.pipelines.YahooStocksPipeline': 391,
        },
        "CLOSESPIDER_ITEMCOUNT": 29
    }
    handle_httpstatus_list = [403,400]

    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='yahoo_stocks_log.txt',format='%(levelname)s: %(message)s',level=logging.INFO,filemode="w+")

    def __init__(self,*args,**kwargs):
        super(YahooStocksSpider,self).__init__(*args,**kwargs)
        self.inputDir = "text_files"
        self.nyseFileName = "nyse.txt"
        self.nasdaqFileName = "nasdaq.txt"
        self.amexFileName = "amex.txt"

        self.name = ""
        self.symbol = ""
        self.price = ""
        self.pointChange = ""
        self.percentChange = ""
        self.previousClosePrice = ""
        self.openPrice = ""
        self.bid = ""
        self.ask = ""
        self.lowDayRange = ""
        self.highDayRange = ""
        self.low52WeekRange = ""
        self.high52WeekRange = ""
        self.volume = ""
        self.averageVolume = ""
        self.marketCap = ""
        self.beta = ""
        self.priceEarningsRatio = ""
        self.earningsPerShare = ""
        self.earningsDate = ""
        self.forwardDividend = ""
        self.yieldPercent = ""
        self.exDividendDate = ""
        self._1YearTarget = ""

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
            # count is the number line in text file
            # nyse.txt, amex.txt, & nasdaq.txt
            count = 0
            print(os.getcwd())
            fileReader = open(os.path.join(self.inputDir,self.amexFileName),"r")
            # skip line
            next(fileReader)
            symbolList = fileReader.readlines()

            for i in symbolList:
                combineStr = ""
                splitStr = i.split("\t")
                symbol = checkEmpty(splitStr[0].strip())
                name = splitStr[1].strip()

                if (symbol != "None"):
                    self.url = "https://finance.yahoo.com/quote/" + symbol
                    # set for read control from file
                    if (count >= 0):
                        yield SplashRequest(url=self.url,callback=self.parseYahooStocks,endpoint="execute", \
                            args={"lua_source": self.script},headers={"User-Agent": random.choice(USER_AGENT_LIST)}, \
                            cb_kwargs={"name": name,"symbol": symbol})

                    count += 1

        except Exception as ex:
            print("exception --- error in start requests => {0}".format(ex))

    def parseYahooStocks(self,response,**args):
        try:
            name = checkEmpty(args["name"])
            setName1(self,name)
            symbol = checkEmpty(args["symbol"])
            setSymbol1(self,symbol)

            setPrice(self,response)
            setPointChange(self,response)
            setPercentChange(self,response)
            setPreviousClosePrice(self,response)
            setOpenPrice(self,response)
            setBid(self,response)
            setDayRange(self,response)
            set52WeekRange(self,response)
            setVolume(self,response)
            setAverageVolume(self,response)
            setMarketCap(self,response)
            setBeta(self,response)
            setPriceEarningsRatio(self,response)
            setEarningsPerShare(self,response)
            setEarningsDate(self,response)
            setForwardDividendAndYield(self,response)
            setExDividendDate(self,response)
            set1YearTarget(self,response)

            loader = loadStocksItem(self,response)
            yield loader.load_item()

        except Exception as ex:
            print("exception => error in parse yahoo --- {0}".format(ex))


