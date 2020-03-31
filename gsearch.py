#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# Modified by JSonWulff
# Based of Meibenjin's orginal code:
# https://github.com/meibenjin/GoogleSearchCrawler
#
# Last updated: 2020-03-31
#
# Google adwords results crawler

import requests
import urllib
import random
import gzip
import io
import time
import re
import xlsxwriter
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

base_url = 'https://www.google.com'

user_agents = list()


class SearchResult:
    def __init__(self):
        self.url = ''

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url

    def printIt(self, prefix=''):
        print('url\t->', self.url, '\n')

    def writeFile(self, filename):
        file = open(filename, 'a')
        try:
            file.write('url:' + self.url + '\n')
        except IOError as e:
            print('file error:', e)
        finally:
            file.close()


class GoogleAPI:
    def __init__(self):
        self.searches = 0

    def randomSleep(self):
        sleeptime = random.randint(60, 120)
        time.sleep(sleeptime)

    def extractSearchResults(self, html):
        results = list()
        soup = BeautifulSoup(html, 'html.parser')

        div = soup.find('div', id='main')
        if (type(div) == type(None)):
            div = soup.find('div', id='center_col')
        if (type(div) == type(None)):
            div = soup.find('body')
        if (type(div) != type(None)):
            ads = div.find_all('span', string="Annonce")

            if (len(ads) > 0):
                for ad in ads:
                    if (type(ads) == type(None)):
                        continue
                    adContainer2 = ad.parent
                    domain = re.search(
                        r'([a-zA-Z0-9-_]+\.*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{1,11}?.\/)', str(adContainer2))
                    results.append(domain.group())

        return results

    def search(self, query, lang='da'):
        search_results = list()
        query = urllib.parse.quote(query)
        url = '%s/search?hl=%s&num=%d&start=%s&q=%s' % (
            base_url, lang, 10, 0, query)
        retry = 3
        while (retry > 0):
            try:
                length = len(user_agents)
                index = random.randint(0, length - 1)
                user_agent = user_agents[index]
                headers = {
                    'user-agent': user_agent,
                    'connection': 'keep-alive',
                    'Accept-Encoding': 'gzip',
                    'referer': base_url
                }
                response = requests.get(url, headers=headers)
                html = response.text
                results = self.extractSearchResults(html)
                search_results.extend(results)
                break
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                self.randomSleep()
                retry = retry - 1
                continue
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.randomSleep()
                retry = retry - 1
                continue
        return search_results


def load_user_agent():
    fp = open('./helperFiles/user_agents.txt', 'r')

    line = fp.readline().strip('\n')
    while (line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()


def load_from_file(path):
    fp = open(path, 'r')

    lines = []

    line = fp.readline().strip('\n')
    while (line):
        lines.append(line)
        line = fp.readline().strip('\n')
    fp.close()

    return lines


def crawler():
    load_user_agent()

    api = GoogleAPI()

    soegeOrd = load_from_file('./searchWords.txt')
    soegeBy = load_from_file('./byer.txt')

    results = []

    workbook = xlsxwriter.Workbook('results.xlsx')

    worksheet = workbook.add_worksheet()

    row = 0
    for word in soegeOrd:
        for by in soegeBy:
            col = 0
            query = (word + ' ' + by)
            print(">> Finding search results for:", query)
            worksheet.write(row, col, query)
            newResult = api.search(query)
            results.extend(newResult)
            for result in newResult:
                col += 1
                worksheet.write(row, col, result)
            row += 1

    workbook.close()
    print(">> Search result are ready in: results.xlsx")


if __name__ == '__main__':
    crawler()
