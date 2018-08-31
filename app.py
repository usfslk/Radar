from flask import Flask, render_template, request
import json, indicoio, sqlite3
from newsapi import NewsApiClient

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
		Score INTEGER
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

	for post in load:
		title = post['title']
		description = post['description']
		url = post['url']
		imglink = post['urlToImage']
		datetime = post['publishedAt']
		scoredesc = indicoio.sentiment(description) * 2
		calc = (scoredesc*100)
		verg = calc / 2
		score = ("%.0f" % verg)
		scorelist.append(float(score))
		nline = title, description, url, imglink, datetime, score
		cursor.execute('INSERT INTO main (Title, Description, URL, IMGLink, Publish, Score) VALUES (?, ?, ?, ?, ?, ?)', (nline))
		conn.commit()
		
	sumlist = (sum(scorelist))
	lenght_list = (len(scorelist))
	before = (sumlist/lenght_list)
	average = float("%.0f" % before) * 2

	for row in cursor.execute("SELECT Title, Description, URL, IMGLink, Score FROM main ORDER BY Score DESC"):
		resultslist.append(row)

	return render_template('main.html', resultslist=resultslist, keyword=keyword, average=average)

@app.route('/results', methods=['GET','POST'])
def results():

	newsapi = NewsApiClient(api_key='b71d9eefeca94a1487e7fc9bf9964af8')
	conn = sqlite3.connect(":memory:")
	cursor = conn.cursor()
	keyword = str(request.args.get( "keyword" , None ))


	cursor.execute(""" 
	CREATE TABLE IF NOT EXISTS main(
		Keyword TEXT UNIQUE,
		Title TEXT,
		Description TEXT,
		URL TEXT,
		IMGLink TEXT,
		Publish TEXT,
		Score INTEGER
	); 
	""")

	data = newsapi.get_everything(q=keyword,
                                      sources='crypto-coins-news',
                                      language='en',
                                      sort_by='publishedAt',
                                      )

	load = data['articles']
	resultslist = []
	scorelist = []

	for post in load:
		title = post['title']
		description = post['description']
		url = post['url']
		imglink = post['urlToImage']
		datetime = post['publishedAt']
		scoredesc = indicoio.sentiment(description) * 2
		calc = (scoredesc*100)
		verg = calc / 2
		score = ("%.0f" % verg)
		scorelist.append(float(score))
		nline = title, description, url, imglink, datetime, score
		cursor.execute('INSERT INTO main (Title, Description, URL, IMGLink, Publish, Score) VALUES (?, ?, ?, ?, ?, ?)', (nline))
		conn.commit()
		
	sumlist = (sum(scorelist))
	lenght_list = (len(scorelist))
	before = (sumlist/lenght_list)
	average = float("%.0f" % before) * 2

	for row in cursor.execute("SELECT Title, Description, URL, IMGLink, Score FROM main ORDER BY Score DESC"):
		resultslist.append(row)

	return render_template('results.html', resultslist=resultslist, keyword=keyword, average=average)


if __name__ == "__main__":
    app.run()
