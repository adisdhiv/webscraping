# -*- coding: utf-8 -*-
import scrapy
import json
import time
from naukriproject.items import NaukriprojectItem


class NaukrispiderSpider(scrapy.Spider):
    name = 'naukrispider'
    url = 'https://www.naukri.com/jobapi/v3/search?noOfResults=500&urlType=search_by_location&searchType=adv&location=india&seoKey=jobs-in-india&src=seo_srp&latLong='
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'systemid': '109',
        'referer': 'https://www.naukri.com/jobs-in-india?l=india',
        'appid': '109',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
     }
    
    def start_requests(self):  
        yield scrapy.Request(url = self.url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        results = json.loads(response.body)
        for i in range(500):
            job = NaukriprojectItem()    
            job['title'] = results['jobDetails'][i]['title']
            job['company'] = results['jobDetails'][i]['companyName']
            job['experience'] = results['jobDetails'][i]['placeholders'][0]['label']
            job['salary'] = results['jobDetails'][i]['placeholders'][1]['label']
            job['joburl'] = results['jobDetails'][i]['jdURL']
            jobid = results['jobDetails'][i]['jobId']
            sid = results['sid']
            next_url = ('https://www.naukri.com/jobapi/v4/job/{}?src=seo_srp&sid={}&xp=1&px=1').format(jobid,sid)
            yield response.follow(next_url, headers = self.headers, meta={'job' : job}, callback = self.parse_detail)

    def parse_detail(self,response):
        result = json.loads(response.body)
        job = response.meta['job']
        job['jobcount'] = result['jobDetails']['applyCount']
        yield job