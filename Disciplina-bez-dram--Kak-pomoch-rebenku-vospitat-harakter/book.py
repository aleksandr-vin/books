# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import logging
import re
import os
from os.path import basename, splitext
from datetime import datetime
from bs4 import BeautifulSoup, NavigableString
import pypandoc

FORMAT = '%(pathname)s:%(lineno)d: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

import requests

def page(n):
    r = requests.get('http://loveread.me/read_book.php?id=50836&p=%d' % (n), allow_redirects=True)
    soup = BeautifulSoup(r.content, 'html.parser')
    text_book = soup.findAll('div', {'class': re.compile("textBook")})[0]
    for e in text_book.findAll('form'):
        e.extract()
    for e in text_book.findAll('div', {'class': re.compile("(navigation|navBlock)")}):
        e.extract()
    return text_book

def img(src, download):
    name = src.split('/')[-1]
    if not download:
        return name
    r = requests.get('http://loveread.me/%s' % (src), allow_redirects=True)
    with open(name, "w+") as f:
        f.write(r.content)
        logging.info("Saved to %s", f.name)
    return name

def html(content):
    return """<!DOCTYPE html>
<head>
<meta charset="UTF-8"/>
</head>
<body>
""" + content + """
</body>
</html>
"""

def download():
    c1 = page(1)
    for p in range(2, 63):
        logging.info("Getting %d page...", p)
        c = page(p)
        c1.append(c)

    with open("out.html", "w+") as out:
        out.write(html(unicode(c1).encode('utf-8')))
        logging.info("Saved to %s", out.name)

def convert():
    with open("out.html", "r") as f:
        data = f.read()
        data = data.replace('\r', ' ')
        soup = BeautifulSoup(data, 'html.parser')
        for e in soup.findAll('div', {'class': re.compile('rdImage')}):
            e.extract()
        titles = soup.findAll('a', {'href': re.compile('view_global.php')})
        for e in titles[1:]:
            e.extract()
        for e in soup.findAll('head'):
            title = soup.new_tag('title')
            title.string = titles[0].string
            e.append(title)
        for e in titles[:1]:
            e.name = 'h1'
            e.attrs = {}
            e.parent.unwrap()
        for e in soup.findAll('div', {'class': re.compile("take_h1")}):
            e.name = 'h2'
            e.attrs = {}
        for e in soup.findAll('img'):
            logging.info("Fetching image %s...", e['src'])
            filename = img(e['src'], True)
            e['src'] = filename
        for e in soup.findAll('div', {'class': re.compile("numberPage")}):
            e.extract()
        for e in soup.findAll('div', {'class': re.compile("textBook")}):
            e.unwrap()
        for e in soup.findAll('h2 h1'):
            e.unwrap()
        for e in soup.findAll('p'):
            e.attrs = {}
        with open("book.html", "w+") as out:
            out.write(unicode(soup).encode('utf-8'))
            logging.info("Saved to %s", out.name)

download()
convert()
