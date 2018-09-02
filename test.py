import dateutil.parser

datestring = '2018-08-31 14:05:19+00:00 '

datetime = dateutil.parser.parse(datestring)

print (datetime.time())