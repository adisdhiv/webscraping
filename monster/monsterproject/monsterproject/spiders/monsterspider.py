# -*- coding: utf-8 -*-
import scrapy
import json
# from bs4 import BeautifulSoup
# from bs4.element import Comment

# def tag_visible(element):
#     if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
#         return False
#     if isinstance(element, Comment):
#         return False
#     return True


# def text_from_html(body):
#     soup = BeautifulSoup(body, 'html.parser')
#     texts = soup.findAll(text=True)
#     visible_texts = filter(tag_visible, texts)  
#     return u" ".join(t.strip() for t in visible_texts)

class MonsterspiderSpider(scrapy.Spider):
    name = 'monsterspider'
    allowed_domains = ['monster.com']
    start_urls = ['https://www.monster.com/jobs/search/pagination/?q=Software-Analyst&where=USA'
                    '&isDynamicPage=true'
                    '&isMKPagination=true'
                    '&page={}'.format(i+1) for i in range(10)]

    def parse(self, response):
        results = json.loads(response.body)
        for result in results:
            try:
                jobId = result['MusangKingId']
            except KeyError:
                continue
            next_url = ('https://job-openings.monster.com/v2/job/pure-json-view?jobid={}').format(jobId)
            yield response.follow(next_url, callback = self.parse_detail)

    def parse_detail(self,response):
        details = {}
        result = json.loads(response.body)
        details['jobId'] = result["jobId"]
        details['title'] = result['companyInfo']['name']
        #details['description'] = text_from_html(result['jobDescription'])
        details['description'] = result['jobDescription']
        info = result['summary']['info']
        for item in info:
            details[item['title']] = item['text']
        yield details

