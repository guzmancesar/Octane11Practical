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
	currency_list = pandas.read_csv('CurrencyCodes.csv')
	#print(currency_list['Currency Code'])
	if options.base not in currency_list.values:
		print("Error: Invalid Base Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")
		quit()


	if isinstance(options.symbol, list):
		for code in options.symbol:
				if code not in currency_list.values:
					print("Error: " + code + " is an invalid Convert Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")	
					quit()
	elif options.symbol not in currency_list.values:
			print("Error" + options.symbol + " is an invalid Convert Currency. Please reference https://taxsummaries.pwc.com/glossary/currency-codes for a list of valid currency codes")	
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
	timedelta = datetime.timedelta(20)
	dateMinusTwenty = currentdate - timedelta
	dateMinusTwenty = dateMinusTwenty.strftime("%Y-%m-%d")
	datePlusTwenty = currentdate + timedelta
	datePlusTwenty = datePlusTwenty.strftime("%Y-%m-%d")

	host = 'https://api.frankfurter.app/'
	if (options.start != None and options.end != None and not(type(options.symbol) is list)):
		response = requests.get('{0}{1}..{2}?from={4},&to={5}'.format(host, options.start, options.end, options.base, options.symbol))
		print(response.content)
	elif (options.start == None):
		print(options.start)
		response = requests.get('{0}{1}'.format(host, dateMinusTwenty, options.end))
		print(response.content)

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

