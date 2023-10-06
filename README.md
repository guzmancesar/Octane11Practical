# Currency Exchanger SP

Local Deployment 

Thank you for using Octane11's premiere command line tool for accessing historical exchange rates. This tool allows a user the ability to reference historical data on currency exchange rates or currency conversion for a specifc rate on a given day. 

The command line tool can be found on https://github.com/guzmancesar/Octane11Practical in its entiretly and can be run on both Zsh(MacOS) or Bash(Linux). You can download each file to a local folder indidually or copy the entire repository using:

" git clone https://github.com/guzmancesar/Octane11Practical.git "

************************************




Testing

The following test cases were run for the history command 

-- standard arguments, 2 symbols provided: PASS
>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD

-- standard arguments, 1 symbols provided: PASS
>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR

-- standard arguments, missing base arg PASS
>$./exrates history --start 2021-02-01 --end 2021-02-02 --symbol EUR CAD

-- standard arguments, fake symbols passed: PASS, error thrown
>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR HFO

-- standard arguments start and end arguments missing, PASS, default dates used
>$./exrates history --base USD --symbol EUR CAD

-- standard arguments start and end arguments missing, PASS, default dates used
>$./exrates history --base USD --symbol EUR CAD

-- standard arguments, missing base currency: PASS default based used
>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD

-- standard arguments, no symbol provided, PASS python throws error because symbol is required
>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD 

Test cases for the convert command 

-- standard arguments, missing base currency: PASS default based used
>$./exrates convert --date 2021-02-01 --symbol EUR  --amount 50

-- standard arguments, multiple symbol args passed: PASS, throws defined error
>$./exrates convert --date 2021-02-01 --symbol EUR GPB --amount 50

-- standard arguments, string as --amount: PASS, python eror thrown regarding type of arg passed
>$./exrates convert --date 2021-02-01 --base USD --symbol EUR  --amount dfgfdbs

-- standard arguments, missing date: PASS, missing date arg used
>$./exrates convert --base USD --symbol EUR  --amount 50





DEPENDENCIES

************************************

- Python3 (Linux)
If you are using Ubuntu 16.10 or newer, then you can easily install Python 3.6 with the following commands:

$ sudo apt-get update
$ sudo apt-get install python3.6

************************************


************************************
- Python3 (MacOS)
https://programwithus.com/learn/python/install-python3-mac
************************************


************************************
- Python Libraries:

you can install the below python modules by running:
"pip install <module name>" for each module below or simply running "pip install -r requirements.txt"

argparse

datetime

requests

************************************






run 'chmod u+r+x exrates' in the directory you have the files stored. If you cloned the
repository with "git clone <link>" it will be in that repository.


Run the program with "./exrates .." followed by the appropriate arguments. 
See below for more information and examples

**************************************

HOW TO RUN THE EXCHANGE RATE TOOL

The tool accepts the following arguments to run for the 'history' command 

start - the start date , default today.

end - the end date , default today.

base - the base currency, default USD.

symbol - the list of currency symbols to convert to (spaces eparated), required.   

output - the file name to write the output to, optional.


EXAMPLE BELOW:

>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD

{"date":"2021-02-01", "base":"USD", "symbol":"CAD", "rate":1.2805362463} 

{"date":"2021-02-01", "base":"USD", "symbol":"EUR", "rate":0.8275405495} 

{"date":"2021-02-02", "base":"USD", "symbol":"CAD", "rate":1.2804716041} 

{"date":"2021-02-02", "base":"USD", "symbol":"EUR", "rate":0.8302889406}


>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD --output output.txt

*saves the ouput to the provided filename instead of printing to the standard output*

***************************************

The tool accepts the following arguments to run for the 'convert' command 



date-the currency exchange date, default today.

base - the base currency, default USD.

symbol- the currency symbol to convert to, required. 

amount-theamounttoconvert, required.

amount - the amount to convert, required


EXAMPLE BELOW:

>$./exrates convert --date 2021-02-01 --base USD --symbol EUR --amount 50

41.377027475
