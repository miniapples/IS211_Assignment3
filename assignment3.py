from io import StringIO

import argparse
import csv
import urllib.request
import re

# this is the URL we are going to use
url = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'

imageTypes = ['.jpg', '.jpeg', '.gif', '.png']
countByBrowser = {
	"firefox": 0,
	"chrome": 0,
	"safari": 0,
	"internet explorer": 0
}
countByHour = {}

def isImageType(pathToFile):
	lowerCase = pathToFile.lower()
	for imageType in imageTypes:
		if imageType in pathToFile:
			return True
	return False

def countBrowser(browser):
	lowerCase = browser.lower()
	for browserType in countByBrowser.keys():
		if browserType in lowerCase:
			countByBrowser[browserType] += 1

def printLargestValue():
	output = ""
	count = 0
	for browserType in countByBrowser.keys():
		if countByBrowser[browserType] > count:
			count = countByBrowser[browserType]
			output = browserType
	return output

def countHits(dateAccessed):
	hour = dateAccessed.split(" ")[1].split(":")[0]
	if int(hour) in countByHour:
		countByHour[int(hour)] += 1
	else:
		countByHour[int(hour)] = 1


def main(url):
	print(f"Running main with URL = {url}...")
	# Open the URL
	response = urllib.request.urlopen(url)
	# Read the response and convert it to string characters if it was in binary
	data = response.read().decode("ascii","ignore")
	# print(data)
	file = StringIO(data)
	reader = csv.reader(file, delimiter=',')
	numImageTypes = 0
	numRows = 0
	for row in reader:
		numRows += 1
		pathToFile = row[0]
		dateAccessed = row[1]
		browser = row[2]
		status = row[3]
		requestSize = row[4]
		if isImageType(pathToFile):
			numImageTypes += 1
		countBrowser(browser)
		countHits(dateAccessed)
	print("Image requests account for " + str(numImageTypes/numRows * 100) + "% of all requests")
	print("The most popular browser is: " + printLargestValue())
	for i in range(0, 24):
		if i in countByHour:
			print("Hour " + str(i) + " has " + str(countByHour[i]) + " hits")
		else:
			print("Hour " + str(i) + " has 0 hits")

if __name__ == "__main__":
	"""Main entry point"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
	args = parser.parse_args()
	main(args.url)
