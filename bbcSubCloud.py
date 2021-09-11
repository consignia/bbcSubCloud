#!/usr/bin/env python3
"""
BBC Sub Cloud
========

Make Word Clouds from BBC Subtitles
"""

#from os import path
from wordcloud import WordCloud
from bs4 import BeautifulSoup as Soup
import urllib
import sys
import json
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

progUrl = 'http://www.bbc.co.uk/programmes/'+ pid +'.json'

info = urllib.request.urlopen(progUrl).read()

infoObj = json.loads(info)

title = infoObj['programme']['title']

print ('Creating Word Cloud For ',title)

camelTitle = camelCase(title)

for version in infoObj['programme']['versions'] :
    pidText = version['pid']
    pidUrl = 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/pc/vpid/' + pidText + '/proto/rtmp?cb=5'
    try:
        extraInfo = urllib.request.urlopen(pidUrl).read()
        extraTree = ET.fromstring(extraInfo)
        captions = extraTree.findall('.//{http://bbc.co.uk/2008/mp/mediaselection}media[@kind=\'captions\']/{http://bbc.co.uk/2008/mp/mediaselection}connection')
        for caption in captions:
            urls.append(caption.get('href'))
    except:
        pass

#Assume the first url is fine

url = urls[0]

print ('Getting Subs from ' + url)

soup = Soup(urllib.request.urlopen(url),features="html.parser")

elements = soup.select('p')

for element in elements:
    for childElement in element.contents:
        grandChildElements = childElement.contents
	    
        if len(grandChildElements) > 0  and isinstance(grandChildElements[0], str):
                text += grandChildElements[0]
                text += ' '

for filteredWord in filteredWords:
    text = text.replace(filteredWord,'')

wordcloud = WordCloud(width=800,height=400).generate(text)

wordcloud.to_file(camelTitle + '.png')


