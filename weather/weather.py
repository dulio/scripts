#!/bin/env python
# -*- coding: utf-8 -*- 
# Filename: weather.py

#####################################
#          Weather Report           #
#               by duliodev.com     #
# @desc: script to fetch data from  #
# http://www.weather.com.cn, and    #
# send mails to users               #
# @datetime: 2013-03-08             #
# @author: dulio                    #
#####################################

import sys
import os
import urllib.request
import json
import mail
import configparser

class weather:
	rawData = None
	def __init__(self, url):
		f = urllib.request.urlopen(url)
		self.rawData = f.read().decode('utf-8')

def parseHTML( vars ):
	weeks = ['星期一','星期二','星期三','星期四','星期五','星期六','星期天']
	
	html = ''
	week = weeks.index( vars['week'] )

	style = '''<style>
</style>
'''

	days = ''
	for day in vars['days']:
		days += '''<tr>
	<td>%s</td>
	<td>%s</td>
	<td>%s</td>
	<td>%s</td>
</tr>
''' % ( weeks[week], day['temp'], day['weather'], day['wind'] )
		week += 1
		if week > 6: week = 0

	html = '''
	%s
	<table border="1px">
		<caption>%s</caption>
		%s
	</table>''' % ( style, vars['city'], days )
	return html

if __name__ == '__main__':
	
	# read configuration file
	config = configparser.ConfigParser()
	config.read( os.path.abspath(os.path.dirname(__file__)) + '/weather.ini')
	
	email_from = config['info']['email_from']
	email_title = ''
	for email, cityids in config['emails'].items():
		cities = []
		html = ''
		for cityid in cityids.split(','):
			''' Prepare weather data '''
			w = weather('http://m.weather.com.cn/data/%s.html' % ( cityid.strip() ))
			# if no content, continue loop
			if w == None: continue

			raw = json.loads( w.rawData )
			raw = raw['weatherinfo']
			# free memory
			del w
			
			# Process weather data
			data = {}
			data['city'] = raw['city']
			cities.append( raw['city'] )
			data['date'] = raw['date']
			data['week'] = raw['week']
			data['days'] = []
			for i in range(1,7):
				day = {}
				day['temp'] = raw['temp' + str(i)]
				day['weather'] = raw['weather' + str(i)]
				day['wind'] = raw['wind' + str(i)]
				data['days'].append(day)

			# Theme weather data
			html += parseHTML( data )
		
		email_title = '| %s | 天气预报 via duliodev.com' % ( ' | '.join(cities) )
		# Send mails to each other
		# print (html)
		mail.send_mail( email_from, email, email_title, html )
		print ('Mail have been sent to %s ( %s )' % ( email, ' | '.join(cities) ) )
