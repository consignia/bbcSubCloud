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

DEFAULT_FILTERED_WORDS = ['LAUGHTER','APPLAUSE']

def camel_case(input):
    output = ''.join(x for x in input.title() if x.isalnum())
    return output[0].lower() + output[1:]

def safe_load(url):
    try:
        url_text = urllib.request.urlopen(url).read()
        return url_text
    except:
        return ''

def get_text_from_bbc_pid(pid):
    urls = []

    text = ''

    #Construct the iplayer url

    prog_url = 'http://www.bbc.co.uk/programmes/'+ pid +'.json'

    info = safe_load(prog_url)

    info_obj = json.loads(info)

    title = info_obj['programme']['title']

    print ('Creating Word Cloud For ',title)

    camel_title = camel_case(title)

    for version in info_obj['programme']['versions'] :
        pid_text = version['pid']
        pid_url = 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/pc/vpid/' + pid_text + '/proto/rtmp?cb=5'
        extra_info = safe_load(pid_url)
        if len(extra_info) > 0:
            extra_tree = ET.fromstring(extra_info)
            captions = extra_tree.findall('.//{http://bbc.co.uk/2008/mp/mediaselection}media[@kind=\'captions\']/{http://bbc.co.uk/2008/mp/mediaselection}connection')
            for caption in captions:
                urls.append(caption.get('href'))


    #Assume the first url is fine

    url = urls[0]

    print('Getting Subs from ' + url)

    soup = Soup(urllib.request.urlopen(url),features="html.parser")

    elements = soup.select('p')

    for element in elements:
        for child_element in element.contents:
            grandchild_elements = child_element.contents
            
            if len(grandchild_elements) > 0  and isinstance(grandchild_elements[0], str):
                    text += grandchild_elements[0]
                    text += ' '

    return text, camel_title

def generate_word_cloud_from_text(text, title, filtered_words):
    for filtered_word in filtered_words:
        text = text.replace(filtered_word,'')

    word_cloud = WordCloud(width=800,height=400).generate(text)

    word_cloud.to_file(title + '.png')

def create_word_cloud_for_pid(pid, filtered_words=[]):
    result = get_text_from_bbc_pid(pid)

    generate_word_cloud_from_text(result[0],result[1],filtered_words)

#Application Entry Point
if len(sys.argv) == 2:
    create_word_cloud_for_pid(sys.argv[1],DEFAULT_FILTERED_WORDS)
else:
    print("Requires extactly one argument")
    print("Usage: ")
    print("python3 bbcSubCloud.py <BBC_PID>")