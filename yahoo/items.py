# define here the models for your scraped items
#
# see documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class StockItem(scrapy.Item):
    company = scrapy.Field()
    symbol = scrapy.Field()
    currentPrice = scrapy.Field()
    previousClosePrice = scrapy.Field()
    openPrice = scrapy.Field()
    bid = scrapy.Field()
    ask = scrapy.Field()
    dayRange = scrapy.Field()
    _52WeekRange = scrapy.Field()
    volume = scrapy.Field()
    averageVolume = scrapy.Field()
    marketCap = scrapy.Field()
    beta = scrapy.Field()
    priceEarningsRatio = scrapy.Field()
    earningsPerShare = scrapy.Field()
    forwardDividend = scrapy.Field()
    yieldPercent = scrapy.Field()