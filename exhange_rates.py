import argparse
import sys
import datetime as dt
import datetime
import requests



def validatea_dates(date_text):
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
	argument_parser.add_argument('--output', required=True)
	return argument_parser.parse_args(args)


options = parse_options(sys.argv[1:])


if options.command != 'history':
	print("Error. Unrecognizd Command: '" + options.command + "'")
	print("Possible command options are: ['history']")
	quit()
if options.start != None and validate_dates(options.start) == False:
	print('Invalid Start Date. Use YYYY-MM-DD as a format and Valid date ranges')
if options.end != None and validate_dates(options.end) == False:
	print('Invalid End Date. Use YYYY-MM-DD as a format and Valid date ranges')
#for base, check if it is a valid currency code
#for symbols check that they are all valid currency codes 
#for output, write to file

host = 'https://api.frankfurter.app'

response = requests.get(host +'/1999-01-04')
print(response.content)

