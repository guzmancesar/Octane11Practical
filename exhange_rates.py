import argparse
import sys
import datetime 
from datetime import date
import datetime
import requests
import pandas



def validate_dates(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True



def parse_options(args):
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument('command')
	argument_parser.add_argument('--start')
	argument_parser.add_argument('--end')
	argument_parser.add_argument('--base', const = 'USD', nargs='?')
	argument_parser.add_argument('--symbol', nargs='*', required = True)
	argument_parser.add_argument('--output')
	return argument_parser.parse_args(args)

def validate_args(options):
	
	#convert options.symbol to list 
	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)

	host = 'https://api.frankfurter.app/'
	endpoint = 'currencies'

	#print(currency_list['Currency Code'])



	if options.base in options.symbol:
		print('Error: Cannot have a base currency in symbols list of currency codes')
		quit()


	if options.base == options.symbol or options.base in options.symbol:
		print("Error: Cannot find exchange rates between identical currencies.")
		quit()

	if options.base not in currency_list.values:
		print("Error: Invalid Base Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")
		quit()

	#use the api for these two if statements 
	for code in options.symbol:
		response = requests.get('{0}{1}'.format(host, endpoint))
		currency_codes = (response.content)
		if code not in currency_codes:
			print("Error: " + code + " is an invalid Convert Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")	
			quit()
	
	if options.command != 'history':
		print("Error: Unrecognizd Command: '" + options.command + "'")
		print("Possible command options are: ['history']")
		quit()
	
	if options.start != None and validate_dates(options.start) == False:
		print('Error: Invalid Start Date. Use YYYY-MM-DD as a format and Valid date ranges')
	
	if options.end != None and validate_dates(options.end) == False:
		print('Error: Invalid End Date. Use YYYY-MM-DD as a format and Valid date ranges')

def getApiContent(options):
	currentdate = date.today()
	currentdate = currentdate.strftime("%Y-%m-%d")
	
	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)

	resultList = []


	host = 'https://api.frankfurter.app/'
	if options.start != None and options.end != None:
		for symbols in options.symbol:
			print(symbols)
			response = requests.get('{0}{1}..{2}?from={3}&to={4}'.format(host, options.start, options.end, options.base, symbols))
			resultList.append(response.content)
	elif (options.start == None):
		for symbols in options.symbol:
			#disclaimer to user -> here
			key = '{0}{1}..{1}?from={2}&to={3}'.format(host, currentdate, options.base, symbols)
			print(key)
			response = requests.get('{0}{1}..{1}?from={2}&to={3}'.format(host, currentdate, options.base, symbols))
			resultList.append(response.content)
	elif (options.end == None):
		for symbols in options.symbol:
			response = requests.get('{0}{1}..{2}?from={4}&to={4}'.format(host, options.start, currentdate, options.base, symbols))
			resultLst.append(response.content)

	#elif (options.end != None):
		#response = requests.get('{0}{1}..{2}'.format(host, options.start, datePlusTwenty))

 

def main():
	options = parse_options(sys.argv[1:])
	validate_args(options)
	getApiContent(options)
	response = requests.get('https://api.frankfurter.app/2020-01-01..2020-01-31?from=USD&to=GBP')
	#print(response.content)


main()
#print(response.content)

