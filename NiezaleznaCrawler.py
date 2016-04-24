# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 19:29:22 2016

@author: piotrgrudzien
"""

from bs4 import BeautifulSoup, Comment
from Utils import removePunct
import urllib2, pickle
import time, datetime

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def niezaleznaCrawl():
    print 'NIEZALEZNA CRAWL'

    link = 'http://niezalezna.pl/'
    
    import sys  

    reload(sys)  
    sys.setdefaultencoding('utf8')
    
    """ Read the main niezalezna page """
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(link)
    
    soup = BeautifulSoup(response, 'lxml')
    
        
    """ Load the timeline from file """
    try:
        Niezalezna_Timeline = pickle.load(open('../Niezalezna/Niezalezna_Timeline.p', 'rb'))
    except IOError:
        print 'Loading empty Niezalezna_Timeline'
        Niezalezna_Timeline = {}
        
    Niezalezna_Urls = []
        
    """ Get the links of the articles you haven't seen before """
    for l in soup.find_all('a'):
        newUrl = l.get('href')
        if(newUrl.startswith(link) & (newUrl != link)):
            Niezalezna_Urls.append(l.get('href'))
        elif((newUrl.startswith('/')) & (is_number(newUrl[1:3]))):
            Niezalezna_Urls.append(link + newUrl[1:])
            
    Niezalezna_Urls = list(set(Niezalezna_Urls))
            
    """ Pickle the updated timeline """
    pickle.dump(Niezalezna_Timeline, open("../Niezalezna/Niezalezna_Timeline.p", "wb"))
       
    """ Get text of each article and write to file """
    print 'Adding', len(Niezalezna_Urls), 'articles'
    for url in Niezalezna_Urls:
        r = opener.open(url)
        soup = BeautifulSoup(r, 'lxml')
        print 'Link:', url

        try:
            title = soup.find(id = 'content').h1.text
        except AttributeError:
            print soup.find(id = 'content').h1
        
        f = open('../Niezalezna/Articles/' + title + '.txt', 'w')
    
        f.write('TITLE:' + removePunct(title.encode('UTF8')) + '\n')
        
        bold = soup.find(id = 'content').strong.text
        f.write('BOLD:' + removePunct(bold) + '\n')
        
        body = ''.join(soup.find("div", {"class":"node-content"}).findAll(text = True, recursive = False)).encode('UTF8')
            
        f.write('BODY:' + body.encode('UTF8'))

        f.close()