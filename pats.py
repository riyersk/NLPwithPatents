#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 08:39:40 2018

@author: subramanianiyer
"""
import scrapy
from itertools import compress
#import wget
from copy import deepcopy
#import zipfile
#import os

class patentSpider(scrapy.Spider):
    name = 'patSpid'
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/' + str(x) + '/' for x in range(1976,2002)]

    def parse(self, response):
        url = response.request.url
        weeks = response.xpath('//div[@class="container"]//a/@href').extract()
        fil = [x[-3:]=='zip' for x in weeks]
        weeks = list(compress(weeks, fil))
        urls = [url + x for x in weeks]
        yield{
                'urls': urls 
        }
