# Octane11Practical

Deployment 

Thank you for using Octane11's premiere command line tool for accessing historical exchange rates. This tool allows a user the ability to reference historical data on currency exchange rates or currency conversion for a specifc rate on a given day. 


************************************

The command line tool can be found on https://github.com/guzmancesar/Octane11Practical in its entiretly and can be run on both Zsh(MacOS) or Bash(Linux). You can download each file to a local folder indidually or copy the entire repository using:

" git clone https://github.com/guzmancesar/Octane11Practical.git "

************************************





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

pandas


************************************



HOW TO RUN THE EXCHANGE RATE TOOL

The tool accepts the following arguments to run

● start - the start date , defaulttoday.
● end - the end date , default today.
● base - the base currency, default USD.
● symbol - the list of currency symbols to convert to (spaces eparated), required.   
● output - the file name to write the output to, optional.


EXAMPLE BELOW:

>$./exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD

{"date":"2021-02-01", "base":"USD", "symbol":"CAD", "rate":1.2805362463} 
{"date":"2021-02-01", "base":"USD", "symbol":"EUR", "rate":0.8275405495} 
{"date":"2021-02-02", "base":"USD", "symbol":"CAD", "rate":1.2804716041} 
{"date":"2021-02-02", "base":"USD", "symbol":"EUR", "rate":0.8302889406}


