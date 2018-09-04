import indicoio, sqlite3
from newsapi import *
import dateutil.parser

#indicoio.config.api_key = '43751098d41ba733826cc75dd3173717'


newsapi = NewsApiClient(api_key='b71d9eefeca94a1487e7fc9bf9964af8')

keyword = "stellar"

pagenum = 1
num_pages = 10


for pagenum in range(2, num_pages + 1):
	
	data = newsapi.get_everything(q=keyword,
                                  language='en',
                                  sources='techcrunch',
                                  page=pagenum,
								  sort_by='publishedAt',
                                  )
	load = data['articles']

	for post in load:
		title = post['title']
		description = post['description'] 
		if keyword in title :
			print(' - ' + title)
			print(description)
			print(' ')
		else: 
			pass