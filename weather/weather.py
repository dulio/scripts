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


def parseHTML( city, vars ):
	html = ''

	style = '''
<style>
	div.city { border-bottom: 0px solid #000; padding: 0.5em }
	div.nighttime { border-bottom: 1px solid #000; }
	h2 { border-bottom: 3px solid #000; }
</style>
'''

	days = ''
	for day in vars:
		if day['title'][-2:] == '夜间':
			mark = 'nighttime'
		else:
			mark = 'daytime'
		days += '''
	<div class="day %s">
		<h4>%s</h4>
		<div>%s</div>
	</div>
''' % ( mark, day['title'], day['fcttext_metric'] )

	html = '''
%s
<div class="city">
	<h2>%s</h2>
	%s
</div>
	''' % ( style, city, days )
	return html

if __name__ == '__main__':
	
	# read configuration file
	config = configparser.ConfigParser()
	config.read( './weather.ini' )
	
	email_from = config['info']['email_from']
	email_title = ''
	for email, cityids in config['emails'].items():
		cities = []
		html = ''
		for cityid in cityids.split(','):
			''' Prepare weather data '''
			api_url = 'http://api.wunderground.com/api/63da66236434d599/forecast/lang:CN/q/%s.json'
			f = urllib.request.urlopen( api_url % ( cityid.strip() ) )
			w = f.read().decode('utf-8')
			# debug data
			# if no content, continue loop
			if w == None: continue

			data = json.loads( w )
			data = data['forecast']['txt_forecast']['forecastday']
			#print(raw)
			# free memory
			del w
			
			# Theme weather data
			html += parseHTML( cityid.strip(), data )
			cities.append( cityid )
		
		email_title = ' %s | Weather Report via mosrv.com' % ( ' | '.join(cities) )
		# Send mails to each other
		#print (html)
		mail.send_mail( email_from, email, email_title, html )
		print ('Mail have been sent to %s ( %s )' % ( email, ' | '.join( cities ) ) )
