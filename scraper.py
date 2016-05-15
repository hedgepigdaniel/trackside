#!/usr/bin/env python

from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request
import re
import sys
from datetime import datetime

REFERRER_URL = "https://tabtrackside.com.au/"
RESULTS_URL = "https://tabtrackside.com.au/results/"

CLASS_RESULTS_ROW = "table--single-result-row"

def getResultsListURL(date):
	url = RESULTS_URL + '?' + 'game_date=' + date
	return url

def getPage(url):
	html = None
	request = urllib.request.Request(url, headers={'Referer': REFERRER_URL})
	with urllib.request.urlopen(request) as response:
		html = response.read()
	return html

def getGameRows(soup):
	return soup.findAll('div', {'class': 'table--single-result-row'})

def makeSoup(html):
	return BeautifulSoup(html, 'lxml')

def getResults(date):
	soup = makeSoup(getPage(getResultsListURL(date)))
	result = {}
	for row in getGameRows(soup):
		grid_items = row.find_all('div', {'class': 'grid__item'})
		text = list(map(lambda node: node.get_text(), grid_items[1:7]))
		print(text)
		gameNumber, race, timeDate, winnerNumber, winnerName, places = text

		try:
			places = list(map(lambda s: {'number': int(s)}, re.split(r',\s*', places)))
		except ValueError:
			continue

		places[0]['name'] = winnerName

		## Exceptions
		if gameNumber == '':
			continue

		gameNumber = int(gameNumber)

		result[gameNumber] = {
			'game': gameNumber,
			'name': race,
			'time': datetime.strptime(timeDate, '%I:%M %p%d-%m-%Y').isoformat(),
			'places': places,
			'detailsURL': grid_items[7].find('a')['href'],
		}
	return result


def main():
	pprint(getResults(sys.argv[1]))

if __name__ == "__main__":
	# execute only if run as a script
	main()
