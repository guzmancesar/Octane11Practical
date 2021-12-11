import argparse
import sys
import datetime 
from datetime import date
import datetime
import requests
import pandas
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



def validate_convert_args(options):
	
	#convert options.symbol to list 
	host = 'https://api.frankfurter.app/'
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



def validate_history_args(options):
	
	#convert options.symbol to list 

	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)


	host = 'https://api.frankfurter.app/'
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



def get_hist_api_content(options):
	currentdate = date.today()
	currentdate = currentdate.strftime("%Y-%m-%d")
	
	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)

	resultList = []


	host = 'https://api.frankfurter.app/'
	for symbols in options.symbol:
		response = requests.get('{0}{1}..{2}?from={3}&to={4}'.format(host, options.start, options.end, options.base, symbols))
		returned_data = json.loads(response.content.decode("utf-8"))
		resultList.append(returned_data)
	
	remoldResults(resultList)
	
	return resultList

	#elif (options.end != None):
		#response = requests.get('{0}{1}..{2}'.format(host, options.start, datePlusTwenty))

def get_conv_api_content(options):
	currentdate = date.today()
	currentdate = currentdate.strftime("%Y-%m-%d")
	
	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)

	host = 'https://api.frankfurter.app/'

	response = requests.get('{0}{1}?from={2}&to={3}'.format(host, options.date, options.base, options.symbol[0]))
	returned_data = json.loads(response.content.decode("utf-8"))


	return returned_data


 

def main():
	options = parse_options(sys.argv[1:])

	if options.command == 'history':
		validate_history_args(options)
		results = get_hist_api_content(options)
	elif options.command == 'convert':
		validate_convert_args(options)
		results = get_conv_api_content(options)
	else:
		print("Error: invalid command. Acceptable command values are ['history', 'convert'])")


main()
#print(response.content)

