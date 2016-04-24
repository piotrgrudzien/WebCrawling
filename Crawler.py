# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 10:28:45 2016

@author: piotrgrudzien

Generic logger (abstract class)
"""

import pickle, urllib2, Utils
from bs4 import BeautifulSoup
from Logger import Logger
import time, datetime


class Crawler:
    def __init__(self, base_link, name):
        self.baseLink = base_link
        self.name = name
        self.mainPage = None
        self.urls = []
        self.logger = None
        self.currentLink = None
        self.title = ''
        self.bold = ''
        self.body = ''

    def crawl(self, logger):
        self.logger = logger # assign logger for this crawl
        self.logger.log(Logger.INFO, 'Starting ' + self.name + ' crawl') # log start of the crawl
        self.urls = [] # prepare empty url list
        self.load_timeline() # load timeline from disk
        self.mainPage = self.read_page(self.baseLink) # load main page
        self.scrape_urls() # get all article urls
        self.urls = list(set(self.urls)) # deduplicate article urls
        for self.currentLink in self.urls:
            print str(self.urls.index(self.currentLink) + 1), '/', str(len(self.urls)) # write out progress to console
            self.logger.log(Logger.INFO, 'Link: ' + self.currentLink) # log info about the article being read
            self.scrape_text(self.currentLink) # get text from the article
            self.clear_text() # remove punctuation, extra spaces, tabs, new-lines
            if self.checks_passed(): # check if article data is valid
                self.save_text() # write article data to file
        self.save_timeline() # save the updated timeline to disk

    def load_timeline(self):
        try:
            self.timeline = pickle.load(open('../' + self.name + '/' + self.name + '_Timeline.p', 'rb'))
        except IOError:
            self.logger.log(Logger.WARN, 'Loading empty ' + self.name + '_Timeline')
            self.timeline = {}

    def save_timeline(self):
        pickle.dump(self.timeline, open('../' + self.name + '/' + self.name + '_Timeline.p', 'wb'))

    def read_page(self, link):
        r = urllib2.urlopen(link).read()
        return BeautifulSoup(r, 'lxml')

    """ Can sometimes be overriden in subclasses """
    def checks_passed(self):
        self.logger.log(Logger.INFO, 'No of words: title - ' + str(len(self.title.split())) + ', bold - ' + str(
            len(self.bold.split())) + ', body - ' + str(len(self.body.split())))
        return str(len(self.title.split())) > 0

    def save_text(self):
        f = open('../' + self.name + '/Articles/' + self.title + '.txt', 'w')
        f.write('TITLE:' + self.title.encode('UTF8') + '\n')
        f.write('BOLD:' + self.bold.encode('UTF8') + '\n')
        f.write('BODY:' + self.body.encode('UTF8'))
        f.close()
        self.timeline[self.currentLink] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def clear_text(self):
        self.title = Utils.clear_text(self.title)
        self.bold = Utils.clear_text(self.bold)
        self.body = Utils.clear_text(self.body)

    """ 'Abstract' method """

    def scrape_urls(self):
        raise Exception('scrapeUrls method not overriden in class', type(self).__name__)

    """ 'Abstract' method """

    def scrape_text(self, link):
        raise Exception('scrapeUrls method not overrident in class', type(self).__name__)
