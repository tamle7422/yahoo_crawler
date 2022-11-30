'''
Define models for your scraped items

see documentation in: https://docs.scrapy.org/en/latest/topics/items.html


'''
import scrapy

class StocksItem(scrapy.Item):
    try:
        name = scrapy.Field()
        symbol = scrapy.Field()
        price = scrapy.Field()
        pointChange = scrapy.Field()
        percentChange = scrapy.Field()
        previousClosePrice = scrapy.Field()
        openPrice = scrapy.Field()
        bid = scrapy.Field()
        ask = scrapy.Field()
        lowDayRange = scrapy.Field()
        highDayRange = scrapy.Field()
        low52WeekRange = scrapy.Field()
        high52WeekRange = scrapy.Field()
        volume = scrapy.Field()
        averageVolume = scrapy.Field()
        marketCap = scrapy.Field()
        beta = scrapy.Field()
        priceEarningsRatio = scrapy.Field()
        earningsPerShare = scrapy.Field()
        earningsDate = scrapy.Field()
        forwardDividend = scrapy.Field()
        exDividendDate = scrapy.Field()
        yieldPercent = scrapy.Field()

    except Exception as ex:
        print("exception --- error in class stocks item => {0}".format(ex))