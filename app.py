# Youssef Selkani

from flask import Flask, render_template, request
import json, indicoio, sqlite3
from newsapi import *

app = Flask(__name__, static_url_path="/static")

indicoio.config.api_key = '43751098d41ba733826cc75dd3173717'
newsapi = NewsApiClient(api_key='b71d9eefeca94a1487e7fc9bf9964af8')

@app.route('/')
def main():	
	conn = sqlite3.connect(":memory:")
	
	cursor = conn.cursor()
	keyword= 'Cryptocurrency'

	cursor.execute(""" 
	CREATE TABLE IF NOT EXISTS main(
		Title TEXT,
		Description TEXT,
		URL TEXT,
		IMGLink TEXT,
		Score INTEGER,
		sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
	); 
	""")

	data = newsapi.get_everything(q=keyword,
	                              language='en',
	                              sources='crypto-coins-news,bloomberg,financial-times,hacker-news',
								  sort_by='publishedAt',
	                              )

	load = data['articles']
	poslist = []
	neglist = []
	scorelist = []
	index = 0
	limit = 20

	for index, post in zip(range(limit), load):
		title = post['title']
		description = post['description']
		url = post['url']
		imglink = post['urlToImage']
		datetime = post['publishedAt']
		scoredesc = indicoio.sentiment(title)
		calc = (scoredesc*100)
		score = ("%.4f" % calc)
		scorelist.append(float(score))
		nline = title, description, url, imglink, score
		cursor.execute('INSERT INTO main (Title, Description, URL, IMGLink, Score) VALUES (?, ?, ?, ?, ?)', (nline))
		conn.commit()

	for row in cursor.execute("SELECT Title, Description, URL, IMGLink, Score, sqltime FROM main  WHERE Score > 60 ORDER BY score DESC LIMIT 4"):
		poslist.append(row)

	for row in cursor.execute("SELECT Title, Description, URL, IMGLink, Score, sqltime FROM main  WHERE Score < 30 ORDER BY score DESC LIMIT 4"):
		neglist.append(row)


	sumlist = (sum(scorelist))
	lenght_list = (len(scorelist))
	before = (sumlist/lenght_list)
	average = float("%.0f" % before) + 10

	return render_template('main.html', poslist=poslist, neglist=neglist, keyword=keyword, average=average)


###

@app.route('/analysis', methods=['GET','POST'])
def results():

	keyword = str(request.args.get( "keyword" , None ))
	conn = sqlite3.connect(":memory:")
	cursor = conn.cursor()
	cursor.execute(""" 
	CREATE TABLE IF NOT EXISTS main(
		Keyword TEXT,
		Title TEXT,
		Description TEXT,
		URL TEXT,
		IMGLink TEXT,
		Score INTEGER,
		sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
	); 
	""")

	resultslist = []
	scorelist = []
	index = 0
	limit = 20

	data = newsapi.get_everything(    q=keyword,
									  sources='crypto-coins-news',
	                                  language='en',
	                                  sort_by='publishedAt',
								 )
	load = data['articles']

	for index, post in zip(range(limit), load):
		title = post['title']
		description = post['description']
		url = post['url']
		imglink = post['urlToImage']
		scoredesc = indicoio.sentiment_hq(title)
		calc = (scoredesc*100)
		score = ("%.2f" % calc)
		scorelist.append(float(score))
		nline = keyword, title, description, url, imglink, score
		cursor.execute('INSERT INTO main (Keyword, Title, Description, URL, IMGLink, Score)  VALUES (?, ?, ?, ?, ?, ?)', (nline))
		conn.commit()

	for row in cursor.execute("SELECT Title, Description, URL, IMGLink, Score, sqltime FROM main ORDER BY Score DESC LIMIT 16"):
		resultslist.append(row)

	sumlist = (sum(scorelist))
	lenght_list = (len(scorelist))
	before = (sumlist/lenght_list)
	average = float("%.0f" % before) + 10

	return render_template('analysis.html', resultslist=resultslist, keyword=keyword, average=average)


@app.route('/analytics')
def analytics():
	return render_template('analytics.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/funding')
def funding():
	return render_template('funding.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/login')
def login():
	return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
