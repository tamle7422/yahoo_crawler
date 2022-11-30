import sys
import os,re
import random
import scrapy
import logging
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.log import configure_logging
from ..hf_yahoo import getLinks,setName,setSymbol,setPointChange,setPercentChange,setPrice,setPreviousClosePrice,setOpenPrice, \
    setBid,setAsk,setDayRange,setMarketCap,set52WeekRange,setVolume,setAverageVolume,setBeta,setPriceEarningsRatio, \
    setEarningsPerShare, \
    setEarningsDate,setForwardDividendAndYield,setExDividendDate,set1YearTarget,checkEmpty,setDate,loadStocksItem,resetStock
from ..settings import USER_AGENT_LIST
from scrapy_splash import SplashRequest,SplashFormRequest

class YahooStocksRuleSpider(CrawlSpider):
    name = "yahoo_rule"
    allowed_domains = ["yahoo.com","finance.yahoo.com"]
    start_urls = ["https://finance.yahoo.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'yahoo.pipelines.YahooStocksRulePipeline': 355,
        },
        "CLOSESPIDER_ITEMCOUNT": 25
    }
    handle_httpstatus_list = [403]

    configure_logging(install_root_handler=False)
    logging.basicConfig(filename="yahoo_rule_log.txt",format='%(levelname)s: %(message)s',level=logging.INFO,filemode="w+")

    # extract links ending with quote and company symbol
    rules = (Rule(LinkExtractor(allow=("quote/"),deny=()),process_request="parseFromRule"),)

    def __init__(self,*args,**kwargs):
        super(YahooStocksRuleSpider,self).__init__(*args,**kwargs)

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
                             -- splash.private_mode_enabled = true
                             -- splash.js_enabled = false
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

    def parseFromRule(self,request,htmlResponse):
        # error: spider must return request, item, or None, got 'generator'
        # return instead of yield generator
        return SplashRequest(url=request.url,callback=self.parseYahoo,endpoint="execute",args={"lua_source": self.script},
             headers={"User-Agent": random.choice(USER_AGENT_LIST)})
        # return scrapy.Request(url=request.url,callback=self.parseYahoo,headers={"User-Agent": random.choice(USER_AGENT_LIST)})

    def parseYahoo(self,response):
        try:
            getLinks(self,response)

            setName(self,response)
            setSymbol(self)
            setPrice(self,response)
            setPointChange(self,response)
            setPercentChange(self,response)
            setPreviousClosePrice(self,response)
            setOpenPrice(self,response)
            setBid(self,response)
            setAsk(self,response)
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