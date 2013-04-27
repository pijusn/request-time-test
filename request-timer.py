#! /usr/bin/python

import sys
import json
import httplib
import time

def readJson(path):
	fin = open(path)
	data = json.load(fin)
	fin.close()
	return data

def getCurrentMilliseconds():
	return int(time.time() * 1000.0)

def request(options):
	startTime = getCurrentMilliseconds()

	conn = httplib.HTTPConnection(options['host'])
	conn.request(options['method'].upper(), options['uri'], options['body'], options['headers'])
	response = conn.getresponse()

	endTime = getCurrentMilliseconds()
	timeTaken = endTime - startTime

	print 'After ' + str(timeTaken) + ' ms: [' + str(response.status) + '] ' + response.reason
	return timeTaken

argc = len(sys.argv)
if (argc == 0):
	print 'This script requires one argument - config file path.'
elif (argc > 2):
	print 'Too many arguments.'
else:
	path = sys.argv[1]
	print 'Loading config file \"' + path + '\"'
	config = readJson(path)

	print 'Requesting http://' + config['host'] + config['uri']

	timeSum = 0
	timeCount = 0
	for i in range(0, config['count']):
		timeTaken = request(config)
		if (timeTaken > 0):
			timeCount += 1
			timeSum += timeTaken
		else:
			print 'Request failed.'

	print str(timeCount) + ' out of ' + str(config['count']) + ' request succeeded.'
	print 'Average request time: ' + str(timeSum / timeCount)

