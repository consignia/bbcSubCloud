#!/usr/bin/env python2
"""
BBC Sub Cloud
========

Make Word Clouds from BBC Subtitles
"""

#from os import path
from wordcloud import WordCloud
from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select
import urllib
import sys

#d = path.dirname(__file__)

# Read the whole text.
#text = open(path.join(d, 'lee.txt')).read()

text = ''

url = sys.argv[1]

print 'Getting Subs from ' + url

soup = Soup(urllib.urlopen(url))

elements = select(soup,'p')

for element in elements:
    for childElement in element.contents:
	if isinstance(childElement, basestring):
            text += childElement
            text += ' '


wordcloud = WordCloud(width=800,height=400).generate(text)

wordcloud.to_file('output.png')

#import matplotlib.pyplot as plt
#plt.imshow(wordcloud)
#plt.axis("off")
#plt.show()
