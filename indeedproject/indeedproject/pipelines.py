# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from twisted.python.compat import unicode
from itemadapter import ItemAdapter

class IndeedprojectPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        company = adapter['company'].split("\n")
        adapter['company']= company[1]
        return item

class CsvPipeline(object):
    def __init__(self):
        self.file = open("jobs.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item