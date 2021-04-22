import pytesseract
from pdf2image import convert_from_path
import glob
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
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

def search(driver, query):
	driver.get("https://www.proquest.com/publication/46852?OpenUrlRefId=info:xri/sid:primo")
	driver.find_element_by_name("publicationQuery").send_keys(query)
	driver.find_element_by_name("publicationQuery").send_keys(Keys.RETURN)

def select_pages(driver):
	time.sleep(4)
	select = Select(driver.find_element_by_id('itemsPerPage')) 
	select.select_by_value('100')

def get_links(driver):
	full_text_elems = driver.find_elements_by_link_text('Full text')
	full_text_links = []
	for elem in full_text_elems:
		full_text_links.append(elem.get_attribute('href'))
		collect_info(elem.get_attribute('href'))
		break
	return full_text_links


def collect_info(link):
	document = {}
	driver.get(link)
	text = driver.find_element_by_id('fullTextZone')
	paras = driver.find_elements_by_css_selector('p')
	text = ''
	for p in paras:
		text += p.text
	print(text)

	



def download_texts(links):
	for url in links:
		article = Article(url)
		title = article.title
		#author = article.author
		keywords = article.keywords
		print(title, keywords)
search(driver, "woodlawn")
select_pages(driver)
links = get_links(driver)
download_texts(links)



def convert_pdfs(path):
	pdfs = glob.glob(r"yourPath\*.pdf")
	for pdf_path in pdfs:
	    pages = convert_from_path(pdf_path, 500)
	    for pageNum,imgBlob in enumerate(pages):
	        text = pytesseract.image_to_string(imgBlob,lang='eng')
	        with open(f'{pdf_path[:-4]}_page{pageNum}.txt', 'w') as the_file:
	            the_file.write(text)

