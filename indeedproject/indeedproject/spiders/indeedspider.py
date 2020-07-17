# -*- coding: utf-8 -*-
import scrapy
from indeedproject.items import IndeedprojectItem

class IndeedspiderSpider(scrapy.Spider):
    name = 'indeedspider'
    allowed_domains = ['indeed.com']
    start_urls = ['http://indeed.com/jobs?q=software+engineer&l=Arizona']    

    def parse(self, response):
        content = response.xpath('//*[@id="resultsCol"]')
        cardcontent = content.css('.jobsearch-SerpJobCard')
        jobdetails = IndeedprojectItem()
        for card in cardcontent:
            companyName = card.css('div > .sjcl > div > span > a::text').get()
            jobdetails['title'] = card.css('h2 > a::attr(title)').get()
            jobdetails['summary'] = card.css('div > .summary > ul > li::text').getall()
            if companyName:
                jobdetails['company'] = companyName   
            else:
                jobdetails['company'] = card.css('div > .sjcl > div > span::text').get()
            yield jobdetails
        nav = content.css('nav > div > ul > li > a::attr(href)').getall()
        nexturl = response.urljoin(nav[-1])
        if nexturl:
            yield response.follow(url = nexturl, callback = self.parse)

        


