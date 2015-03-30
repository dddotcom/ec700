import json
import scrapy
import re
from pprint import pprint
from tutorial.items import GoogleItem

login_pages = []
facebook_signin = "https://www.google.com/search?q=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&oq=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&num=100&start=300&aqs=chrome..69i57.987j0j1&sourceid=chrome&es_sm=93&ie=UTF-8"
google_signin = "https://www.google.com/search?q=sign+in+with+google+inurl%3A%2Fsignin%2F+-site%3Agoogle.com+-site%3Agithub.com+-site%3Astackoverflow.com&oq=sign+in+with+google+inurl%3A%2Fsignin%2F+-site%3Agoogle.com+-site%3Agithub.com+-site%3Astackoverflow.com&num=100&start=100&aqs=chrome..69i57.2198j0j9&sourceid=chrome&es_sm=93&ie=UTF-8"
twitter_login = "https://www.google.com/search?q=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&oq=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&num=100&start=100&aqs=chrome..69i57.275j0j1&sourceid=chrome&es_sm=93&ie=UTF-8#q=%22with+twitter%22+inurl:%22%2Flogin%22+-site:twitter.com"

#idp="twitter" #facebook, google 

def get_sites_for_idp(idp):
	if "twitter" in idp:
		return "../twitter_sites.json"
	if "facebook" in idp:
		return "../facebook_sites.json"
	if "google" in idp:
		return "../google_sites.json"

def find_login_pages(idp):
	print "opening " + get_sites_for_idp(idp) + "..."
	with open(get_sites_for_idp(idp)) as data_file:    
	    data = json.load(data_file)

	f = open('check_these_sites.txt','w')
	for d in data:
		if "/login&sa=" in str(d["link"]) or "/login/&sa=" in str(d["link"]) or "/signin&sa=" in str(d["link"]) or "/signin/&sa=" in str(d["link"]):
			login_pages.append(re.search("(?P<url>https?://[^\s]+)", str(d["link"])).group("url").split("&sa=")[0])
			f.write(re.search("(?P<url>https?://[^\s]+)", str(d["link"])).group("url").split("&sa=")[0] + '\n') # python will convert \n to os.linesep
	#print login_pages
	f.close()

def get_start_urls():

	array = []
	with open("check_these_sites.txt", "r") as f:	
		for line in f.read().splitlines():
			array.append(line)
	f.close()
	print array

def generate_unique_url_list(json_file):
	unique_urls = set()
	with open(json_file) as data_file:    
	    data = json.load(data_file)
	for d in data:
		unique_urls.add(str(d["link"]))

	f = open('final_check_these_sites.txt','w')
	for url in unique_urls:
		f.write(url + '\n')
	f.close()

def get_many_results():
	num_sites = 1000
	start_urls = []
	for i in range(num_sites/100):
		new_url = "https://www.google.com/search?q=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&oq=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&num=100&start=" + str(i*100) + "&aqs=chrome..69i57.987j0j1&sourceid=chrome&es_sm=93&ie=UTF-8"
		start_urls.append(new_url)
	
	f = open('generated_urls.txt','w')
	f.write("start_urls = [" + "\n")
	for url in start_urls:
		if url == start_urls[-1]:
			f.write('\t"' + url + '"\n')
		else:
			f.write('\t"' + url + '",\n')
	f.write("]")
	f.close()

get_many_results()
