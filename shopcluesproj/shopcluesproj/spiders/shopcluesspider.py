# -*- coding: utf-8 -*-
import scrapy
from shopcluesproj.items import ShopcluesprojItem
from scrapy_splash import SplashRequest


class ShopcluesspiderSpider(scrapy.Spider):
    name = 'shopcluesspider'
    allowed_domains = ['www.shopclues.com']
    start_urls = ['https://www.shopclues.com/clocks.html']

    def parse(self, response):
        title =  response.css(".prod_name ::text").extract()
        price = response.css(".p_price::text").extract()
        discount = response.css(".prd_discount::text").extract()
        oldprice = response.css("div.old_prices span::text").extract()
        product = ShopcluesprojItem()
        for i in range(len(title)):
            product['title'] = title[i]
            product['price'] = price[i]
            product['discount'] = discount[i]
            product['oldprice'] = oldprice[i]
            yield product

