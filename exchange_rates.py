#!/usr/bin/env python

import argparse
import sys
import datetime 
from datetime import date
import datetime
import requests
import json



def validate_dates(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

def remoldResults(resultList):

	finalResults = []

	for resultset in resultList:
		#for (date, symbol, rates) in zip (resultset['rates'], resultset['rates'].values().keys(), resultset['rates'].values().values()):
			#print(date, symbol, rates)

		if len(resultset) == 4:
			rate_list  = {"date":resultset['date'], "base":resultset['base'], "symbol":str(list(resultset['rates'].keys())[0]), "rate":str(list(resultset['rates'].values())[0])}
			finalResults.append(rate_list)
		else:
			for (date,data) in zip(resultset['rates'].values(), resultset['rates']):
				rate_list = {"date":str(data), "base":str(resultset['base']), "symbol":str(list(date.keys())[0]), "rate":str(list(date.values())[0])}
				finalResults.append(rate_list)

	final_results_sorted = sorted(finalResults, key = lambda i: (i['date'], i['symbol']))
	return final_results_sorted


def parse_options(args):

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest="command")
	

	parser_history = subparsers.add_parser('history')
	parser_history.add_argument('--start', default = date.today().strftime("%Y-%m-%d"))
	parser_history.add_argument('--end', default = date.today().strftime("%Y-%m-%d"))
	parser_history.add_argument('--base', default = 'USD', nargs='?')
	parser_history.add_argument('--symbol', nargs='*', required = True)
	parser_history.add_argument('--output')

	convert_parser = subparsers.add_parser('convert')
	convert_parser.add_argument('--date', default = date.today().strftime("%Y-%m-%d"), nargs = '?')
	convert_parser.add_argument('--base', default = 'USD', nargs='?')
	convert_parser.add_argument('--symbol', nargs='*', required = True)
	convert_parser.add_argument('--amount', type=int, required = True)

	#print(parser.parse_args(args))
	return parser.parse_args(args)



def validate_convert_args(options, host):
	
	#convert options.symbol to list 
	endpoint = 'currencies'
	response = requests.get('{0}{1}'.format(host, endpoint))
	currency_codes = list(json.loads(response.content.decode("utf-8")).keys())

	if len(options.symbol) > 1:
		print("Error: Invalid arguments for the --symbol flag. The 'convert' command will only accept one 'symbol' argument")
		quit()

	if options.base in options.symbol:
		print("Error: Cannot have identical currencies in --base and --symbol arguments")
		quit()

	if options.date != None and validate_dates(options.date) == False:
		print('Error: Invalid Date. Use YYYY-MM-DD as a format and Valid date ranges')		
		quit()

	if options.base not in currency_codes:
		print("Error: Invalid Base Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")
		quit()

	#use the api for these two if statements 
	for code in options.symbol:
		if code not in currency_codes:
			print("Error: " + code + " is an invalid Convert Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")	
			quit()
	
	#if not isinstance(options.amount, int):
	#	print("Error: {0} is not a valid argument for the --amount flag. Please provide integers for this argument".format(options.amount))
	#	quit()
	#commenting this function out, python will throw an error if the --amount arg is not an int so this funciton is 
	#redundant 



def validate_history_args(options, host):
	
	#convert options.symbol to list 

	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)


	endpoint = 'currencies'
	response = requests.get('{0}{1}'.format(host, endpoint))
	currency_codes = list(json.loads(response.content.decode("utf-8")).keys())


	if options.base in options.symbol:
		print('Error: Cannot have a base currency in symbols list of currency codes')
		quit()

	if options.base not in currency_codes:
		print('Error: '  + options.base + 'is an invalid Currency. Please see the below for a list of valid currency codes')
		quit()

	#use the api for these two if statements 
	for code in options.symbol:
		if code not in currency_codes:
			print('Error: ' + code + 'is an invalid Currency. Please see the below for a list of valid currency codes')	
			quit()
	
	if options.start != None and validate_dates(options.start) == False:
		print('Error: Invalid Start Date. Use YYYY-MM-DD as a format and Valid date ranges')
	
	if options.end != None and validate_dates(options.end) == False:
		print('Error: Invalid End Date. Use YYYY-MM-DD as a format and Valid date ranges')



def get_hist_api_content(options, host):
	resultList = []

	if options.start > options.end:
		print('Error: Unable to use start date as it takes place after provided end date. Reassiging start date to be equivalent to end date')
		options.start = options.end
	for symbols in options.symbol:
		if options.start == options.end:
			response = requests.get('{0}{1}?from={2}&to={3}'.format(host, options.start, options.base, symbols))
		else:
			response = requests.get('{0}{1}..{2}?from={3}&to={4}'.format(host, options.start, options.end, options.base, symbols))
		returned_data = json.loads(response.content.decode("utf-8"))
		resultList.append(returned_data)
	
	#print(resultList)

	return(remoldResults(resultList))

	#elif (options.end != None):
		#response = requests.get('{0}{1}..{2}'.format(host, options.start, datePlusTwenty))

def get_conv_api_content(options, host):


	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)


	response = requests.get('{0}{1}?from={2}&to={3}'.format(host, options.date, options.base, options.symbol[0]))
	returned_data = json.loads(response.content.decode("utf-8"))

	conversion_rate = list(returned_data["rates"].values())[0]


	return (options.amount * conversion_rate)


 

def main():
	options = parse_options(sys.argv[1:])
	apiHost =  'https://api.frankfurter.app/'

	if options.command == 'history':
		validate_history_args(options, apiHost)
		results = get_hist_api_content(options, apiHost)
		if options.output != None:
			
			fileToWrite = open(options.output, "w")

			for record in results:
				fileToWrite.write(str(record))
				fileToWrite.write('\n')
			
			fileToWrite.close()

		else:
			
			for record in results:
				print(record)

	elif options.command == 'convert':
		validate_convert_args(options, apihost)
		results = get_conv_api_content(options, apiHost)
		print(results)
	else:
		print("Error: invalid command. Acceptable command values are ['history', 'convert'])")


main()
#print(response.content)

