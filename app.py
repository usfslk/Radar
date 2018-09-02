from flask import Flask, render_template, request
import json, indicoio, sqlite3
from newsapi import *
from dateutil.parser import *

app = Flask(__name__, static_url_path="/static")

indicoio.config.api_key = '43751098d41ba733826cc75dd3173717'

@app.route('/')
def main():	
	conn = sqlite3.connect(":memory:")
	cursor = conn.cursor()
	keyword = str(request.args.get( "keyword" , None ))
	newsapi = NewsApiClient(api_key='b71d9eefeca94a1487e7fc9bf9964af8')

	cursor.execute(""" 
	CREATE TABLE IF NOT EXISTS main(
		Keyword TEXT UNIQUE,
		Title TEXT,
		Description TEXT,
		URL TEXT,
		IMGLink TEXT,
		Publish TEXT,
		Score INTEGER, 
		IndexLine INTEGER
	); 
	""")

	data = newsapi.get_everything(
                                      sources='crypto-coins-news',
                                      language='en',
                                      sort_by='publishedAt',
                                      )

	load = data['articles']
	resultslist = []
	scorelist = []
	index = 0
	limit = 3

	for index, post in zip(range(limit), load):
		title = post['title']
		description = post['description']
		url = post['url']
		imglink = post['urlToImage']
		dateparse = post['publishedAt']
		datetime = str(dateutil.parser.parse(dateparse).time())
		scoredesc = indicoio.sentiment(description) * 1.5
		calc = (scoredesc*100)
		verg = calc / 2
		score = ("%.0f" % verg)
		scorelist.append(float(score))
		nline = title, description, url, imglink, datetime, score, index
		cursor.execute('INSERT INTO main (Title, Description, URL, IMGLink, Publish, Score, IndexLine) VALUES (?, ?, ?, ?, ?, ?, ?)', (nline))
		conn.commit()
		
	sumlist = (sum(scorelist))
	lenght_list = (len(scorelist))
	before = (sumlist/lenght_list)
	average = float("%.0f" % before) * 1.5

	for row in cursor.execute("SELECT Title, Description, URL, IMGLink, Score, Publish FROM main ORDER BY Score DESC"):
		resultslist.append(row)

	return render_template('main.html', resultslist=resultslist, keyword=keyword, average=average)


############

@app.route('/analysis', methods=['GET','POST'])
def results():
	keyword = str(request.args.get( "keyword" , None ))
	newsapi = NewsApiClient(api_key='b71d9eefeca94a1487e7fc9bf9964af8')
	conn = sqlite3.connect(":memory:")
	cursor = conn.cursor()
	cursor.execute(""" 
	CREATE TABLE IF NOT EXISTS main(
		Keyword TEXT UNIQUE,
		Title TEXT,
		Description TEXT,
		URL TEXT,
		IMGLink TEXT,
		Publish TEXT,
		Score INTEGER,
		IndexLine INTEGER
	); 
	""")
	data = newsapi.get_everything(q=keyword,
                                      sources='crypto-coins-news',
                                      language='en',
                                      sort_by='relevancy',
								)
	load = data['articles']
	resultslist = []
	scorelist = []
	index = 0
	limit = 1

	for index, post in zip(range(limit), load):
		title = post['title']
		description = post['description']
		datasource = str(post['source'])
		url = post['url']
		imglink = post['urlToImage']
		dateparse = post['publishedAt']
		datetime = str(dateutil.parser.parse(dateparse).time())
		scoredesc = indicoio.sentiment(description) * 1.5
		calc = (scoredesc*100)
		verg = calc / 2
		score = ("%.0f" % verg)
		scorelist.append(float(score))
		nline = title, description, url, imglink, datetime, score
		cursor.execute('INSERT INTO main ( Title, Description, URL, IMGLink, Publish, Score) VALUES (?, ?, ?, ?, ?, ?)', (nline))
		conn.commit()
		
	sumlist = (sum(scorelist))
	lenght_list = (len(scorelist))
	before = (sumlist/lenght_list)
	average = float("%.0f" % before) * 1.5

	for row in cursor.execute("SELECT Title, Description, URL, IMGLink, Score, Publish FROM main ORDER BY Score DESC"):
		resultslist.append(row)

	return render_template('analysis.html', resultslist=resultslist, keyword=keyword, average=average)


@app.route('/analytics')
def analytics():
	return render_template('analytics.html')

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
