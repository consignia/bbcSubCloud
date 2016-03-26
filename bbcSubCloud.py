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
import xml.etree.ElementTree as ET

def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

filteredWords = ['LAUGHTER','APPLAUSE']

text = ''

#Gather Caption urls

urls = []

pid = sys.argv[1]

#Construct the iplayer url

progUrl = 'http://www.bbc.co.uk/programmes/'+ pid +'.xml'

info = urllib.urlopen(progUrl).read()

infoTree = ET.fromstring(info)

title = infoTree.findall('.//display_title/title')[0].text + ' : ' + infoTree.findall('.//display_title/subtitle')[0].text

print 'Creating Word Cloud For ' + title

camelTitle = camelCase(title)

for element in infoTree.findall('.//versions/version/pid') :
    pidText = element.text
    pidUrl = 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/pc/vpid/' + pidText + '/proto/rtmp?cb=5'
    extraInfo = urllib.urlopen(pidUrl).read()
    extraTree = ET.fromstring(extraInfo)
    captions = extraTree.findall('.//{http://bbc.co.uk/2008/mp/mediaselection}media[@kind=\'captions\']/{http://bbc.co.uk/2008/mp/mediaselection}connection')
    for caption in captions:
        urls.append(caption.get('href'))

#Assume the first url is fine

url = urls[0]

print 'Getting Subs from ' + url

soup = Soup(urllib.urlopen(url))

elements = select(soup,'p')

for element in elements:
    for childElement in element.contents:
	if isinstance(childElement, basestring):
            text += childElement
            text += ' '

for filteredWord in filteredWords:
    text = text.replace(filteredWord,'')

wordcloud = WordCloud(width=800,height=400).generate(text)

wordcloud.to_file(camelTitle + '.png')


