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



def parse_options(args):
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument('command')
	argument_parser.add_argument('--start')
	argument_parser.add_argument('--end')
	argument_parser.add_argument('--base', const = 'USD', nargs='?')
	argument_parser.add_argument('--symbol', nargs='*', required = True)
	argument_parser.add_argument('--output')
	argument_parser.add_argument('--date')
	argument_parser.add_argument('--amount', type=int)


	return argument_parser.parse_args(args)



def validate_convert_args(options):
	
	#convert options.symbol to list 
	if len(options.symbol) > 1:
		print("Error: Invalid arguments for the --symbol flag. The 'convert' command will only accept one 'symbol' argument")
		quit()

	host = 'https://api.frankfurter.app/'
	endpoint = 'currencies'
	response = requests.get('{0}{1}'.format(host, endpoint))
	currency_codes = list(json.loads(response.content.decode("utf-8")).keys())


	#print(currency_list['Currency Code'])


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
	

	if not isinstance(options.amount, int):
		print("Error: {0} is not a valid argument for the --amount flag. Please provide integers for this argument".format(options.amount))
		quit()




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


	#use the api for these two if statements 
	for code in options.symbol:
		if code not in currency_codes:
			print("Error: " + code + " is an invalid Convert Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")	
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
	if options.start != None and options.end != None:
		for symbols in options.symbol:
			response = requests.get('{0}{1}..{2}?from={3}&to={4}'.format(host, options.start, options.end, options.base, symbols))
			resultList.append(response.content)
	elif (options.start == None):
		for symbols in options.symbol:
			#disclaimer to user -> here
			key = '{0}{1}..{1}?from={2}&to={3}'.format(host, currentdate, options.base, symbols)
			response = requests.get('{0}{1}..{1}?from={2}&to={3}'.format(host, currentdate, options.base, symbols))
			resultList.append(response.content)
	elif (options.end == None):
		for symbols in options.symbol:
			response = requests.get('{0}{1}..{2}?from={3}&to={4}'.format(host, options.start, currentdate, options.base, symbols))
			resultList.append(response.content)

	return resultList

	#elif (options.end != None):
		#response = requests.get('{0}{1}..{2}'.format(host, options.start, datePlusTwenty))

def get_conv_api_content(options):
	currentdate = date.today()
	currentdate = currentdate.strftime("%Y-%m-%d")
	
	if not(type(options.symbol) is list):
		options.symbol = list(options.symbol)

	resultList = []


	host = 'https://api.frankfurter.app/'
	if options.start != None and options.end != None:
		for symbols in options.symbol:
			response = requests.get('{0}{1}..{2}?from={3}&to={4}'.format(host, options.start, options.end, options.base, symbols))
			resultList.append(response.content)
	elif (options.start == None):
		for symbols in options.symbol:
			#disclaimer to user -> here
			key = '{0}{1}..{1}?from={2}&to={3}'.format(host, currentdate, options.base, symbols)
			response = requests.get('{0}{1}..{1}?from={2}&to={3}'.format(host, currentdate, options.base, symbols))
			resultList.append(response.content)
	elif (options.end == None):
		for symbols in options.symbol:
			response = requests.get('{0}{1}..{2}?from={3}&to={4}'.format(host, options.start, currentdate, options.base, symbols))
			resultList.append(response.content)

	return resultList


 

def main():
	options = parse_options(sys.argv[1:])

	if options.command == 'history':
		validate_history_args(options)
		results = get_hist_api_content(options)
		print(results)
	elif options.command == 'convert':
		validate_convert_args(options)
		results = get_conv_api_content(options)
		print(results)
	else:
		print("Error: invalid command. Acceptable command values are ['history', 'convert'])")


main()
#print(response.content)

