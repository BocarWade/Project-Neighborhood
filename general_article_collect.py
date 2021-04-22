import requests
import pandas as pd
from PIL import ImageTk, Image
import os
from io import BytesIO
import urllib
import PIL
from newsapi.newsapi_client import NewsApiClient
from newspaper import Article
#from geotext import GeoText
import nltk
from nltk import tokenize
from requests import get
#from mordecai import Geoparser
# @article{halterman2017mordecai,
#   title={Mordecai: Full Text Geoparsing and Event Geocoding},
#   author={Halterman, Andrew},
#   journal={The Journal of Open Source Software},
#   volume={2},
#   number={9},
#   year={2017},
#   doi={10.21105/joss.00091}
# }

key = '025512d2e135410786a6be81ce08efd7'

def get_sentances(text):
	""" Seprates bock of text into sentances 
	@param text (string): the common name of the plant you want to search  
	@returns out (lists(strings)): A list of strings that have been delimeted by punctuation
	"""
	return tokenize.sent_tokenize(p)
	

def search_n_hood(name):
	""" Searches for a query using newspaper api
	@param name (string): the name of the search term which you itnend to use
	@returns out (dictionary): a dictionary containing information about the article
	"""
	newsapi = NewsApiClient(api_key=key)
	top_headlines = newsapi.get_everything(q=name, language='en', page_size=100)
	print(len(top_headlines['articles']))nay
	return top_headlines


def download_articles(query, articles):
	""" Downloads all the articles present in the results from the query
	@param articles (dicitonary): the dictionary of all the articles found from query
	@returns out (None):
	"""
	for i in range(len(articles)):
		print(i)
		# the title associated with article
		title = articles[i]['title'] or "None"
		# the name of person who wrote article
		author = articles[i]['author'] or "None"
		# the new outlet that published articles
		source = articles[i]['source']['name'] or "None"
		date = articles[i]['publishedAt'] or "None"
		sep = '----------------------------'
		url = articles[i]['url']
		article = Article(url)
		try:
			article.download()
		except:
			continue
		try:
			article.parse()
		except:
			continue
		content = article.text or "None"
		filename = "Articles/{query}/{name}.txt".format(query = query, name = title[0:20])
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		new_file = open(filename,"w")
		article_info = [title + '\n', author + '\n', date + '\n', sep + '\n', content + '\n'] 
		for segment in article_info:
			new_file.write(segment) 
		new_file.close()



def extract_atttribute(text):
	""" The following uses geoparisng to extract the name of the entity and 
	determine its geographic location and bounds
	@param text (string): the textt from the article which will be geoparsed
	@returns out (dictionary): information formated regarding what has been parsed
	"""
	geo = Geoparser()
	results = geo.geoparse(text)
	print(results)

def main():
	#extract_atttribute("I traveled from Oxford to Ottawa.")
	#extract_atttribute("I traveled to Bushwick New York")
	name = input("What neighbrohood city would you like to search for? Z to quit: ")
	while name.lower() != "z":
		print("Searching for {name} ... ".format(name = name))
		results = search_n_hood(name) 
		num_articles = results['totalResults']
		articles = results['articles']
		print("We found {num} articles mentioning {name}".format(num = num_articles, name = name))
		print("Downloading articles ... ")
		download_articles(name, articles)
		name = input("What neighbrohood city would you like to search for? Z to quit: ")


if __name__ == "__main__":
	main()

