from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import pandas as pd
from newspaper import Config, Article, Source
import newspaper
from selenium.webdriver.common.keys import Keys
import time 

QUERY = "bayview"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('/Users/bocarwade/Downloads/chromedriver')
#driver.get(webiste)

def site_login():
	username = "bocarw99@stanford.edu"
	password = "ProjectNeighborhood123"
	driver.get("https://www.sfchronicle.com/")
	signIn_butt = driver.find_elements_by_xpath('/html/body/header/div[4]/ul/li[3]/div[1]')
	signIn_butt[0].click()
	window_after = driver.window_handles[1]
	driver.switch_to.window(window_after)
	time.sleep(1)
	driver.find_element_by_id("email").send_keys(username)
	driver.find_element_by_id("password").send_keys(password)
	driver.find_element_by_id("signInSubmit").click()
	window_after = driver.window_handles[0]
	driver.switch_to.window(window_after)


def search(driver, query):
	time.sleep(1)
	driver.find_elements_by_xpath("/html/body/header/div[4]/ul/li[4]")[0].click()
	time.sleep(1)
	driver.find_element_by_name("query").send_keys(query)
	driver.find_element_by_name("query").send_keys(Keys.RETURN)

def collect_articles(driver, url):
	artice_divs = driver.find_elements_by_xpath("/html/body/div[2]/div[2]")
	config = Config()
	config.memoize_articles = False
	config.request_timeout = 7
	site = newspaper.build(url,memoize_articles = False)
	articles = site.article_urls()
	print(len(articles))
	print(articles)
	return articles

def load_articles(driver):
	hRefs = []
	parent = driver.find_element_by_class_name("content")
	while True:
		try:
			loadMoreButton = driver.find_element_by_class_name("more-btn")
			loadMoreButton.click() 
			time.sleep(2)
		except Exception as e:
			print(e)
			break
	for link in links:
		hRefs.append(link)
	print(len(hRefs))
	print(hRefs)
	return hRefs

def download_articles(urls, query):
	for article in urls:
		article = Article(url)
		try:
			article.download()
		except Exception as e:
			print(e)
		try:
			article.parse()
		except Exception as e:
			print(e)
		content = article.text or "None"
		title = article.title
		author = article.author
		keywords = article.keywords 
		filename = "Articles/{query}/{name}.txt".format(query = query, name = title[0:20])
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		new_file = open(filename,"w")
		article_info = [title + '\n', author + '\n', date + '\n', sep + '\n', content + '\n'] 
		for segment in article_info:
			new_file.write(segment) 
		new_file.close()

site_login()
search(driver, "bayview")
load_articles(driver)
download_articles(urls, query)
driver.quit()
