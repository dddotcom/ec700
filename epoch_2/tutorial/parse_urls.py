import json
import scrapy
import re
from pprint import pprint
from tutorial.items import GoogleItem

login_pages = []

def find_login_pages():
	with open('out.json') as data_file:    
	    data = json.load(data_file)

	f = open('check_these_sites.txt','w')
	for d in data:
		if "/login&sa=" in str(d["link"]) or "/login/&sa=" in str(d["link"]):
			login_pages.append(re.search("(?P<url>https?://[^\s]+)", str(d["link"])).group("url").split("&sa=")[0])
			f.write(re.search("(?P<url>https?://[^\s]+)", str(d["link"])).group("url").split("&sa=")[0] + '\n') # python will convert \n to os.linesep
	print login_pages
	f.close() # you can omit in most cases as the destructor will call if

def get_start_urls():

	array = []
	with open("check_these_sites.txt", "r") as f:	
		for line in f.read().splitlines():
			array.append(line)
	f.close()
	print array

def generate_unique_url_list():
	unique_urls = set()
	with open('oauth_sites.json') as data_file:    
	    data = json.load(data_file)
	for d in data:
		unique_urls.add(str(d["link"]))

	f = open('final_check_these_sites.txt','w')
	for url in unique_urls:
		f.write(url + '\n') # python will convert \n to os.linesep
	f.close()