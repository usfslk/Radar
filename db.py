import sqlite3
from newsapi import *


newsapi = NewsApiClient(api_key='b71d9eefeca94a1487e7fc9bf9964af8')

conn = sqlite3.connect("forloop.db")
cursor = conn.cursor()
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS main(
	ID int(11),
	Keyword TEXT,
	Title varchar(255) UNIQUE,
	Description TEXT,
	sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
); 
""")

resultslist = []
scorelist = []

index = 0
limit = 20
pagenum = 1
num_pages = 10

keyword = 'Monero'

for pagenum in range(2, num_pages + 1):
	print('page: ' + str(pagenum))
	data = newsapi.get_everything(    sources='crypto-coin-news',
	                                  language='en',
	                                  sort_by='publishedAt',
	                                  page=pagenum,
	                                  q=keyword
								 )
	load = data['articles']


	for index, post in zip(range(limit), load):
		title = post['title']
		description = post['description']
		if len(cursor.execute("SELECT Title FROM main WHERE Title = ?", (title,)).fetchall())  > 0:
			pass
		else:
			if keyword in title:
				nline = keyword, title, description
				cursor.execute('INSERT INTO main (Keyword, Title, Description)  VALUES (?, ?, ?)', (nline))
				conn.commit()
				print('db +')
			else:
				pass			
	
for row in cursor.execute("SELECT Title, Description, sqltime FROM main ORDER BY sqltime DESC"):
	resultslist.append(row)

