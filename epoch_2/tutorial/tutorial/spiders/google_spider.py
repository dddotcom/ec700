import scrapy
import json
from pprint import pprint
from tutorial.items import GoogleItem

class GoogleSpider(scrapy.Spider):
	name = "google"
	allowed_domains = ["https://www.google.com"]
	start_urls = [
		"https://www.google.com/search?q=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&oq=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&num=100&start=900&aqs=chrome..69i57.987j0j1&sourceid=chrome&es_sm=93&ie=UTF-8&filter=0"
	]
	# start_urls = []
	# with open("generated_urls.txt", "r") as f:	
	# 	for line in f.read().splitlines():
	# 		start_urls.append(line)
	# f.close()
	# print start_urls


#google signin
# "https://www.google.com/search?q=sign+in+with+google+inurl%3A%2Fsignin%2F+-site%3Agoogle.com+-site%3Agithub.com+-site%3Astackoverflow.com&oq=sign+in+with+google+inurl%3A%2Fsignin%2F+-site%3Agoogle.com+-site%3Agithub.com+-site%3Astackoverflow.com&num=100&start=100&aqs=chrome..69i57.2198j0j9&sourceid=chrome&es_sm=93&ie=UTF-8"
#facebook signin
# "https://www.google.com/search?q=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&oq=sign+in+with+facebook+inurl%3A%2Fsignin%2F+-site%3Afacebook.com+-site%3Agithub.com+-site%3Astackoverflow.com&num=100&start=900&aqs=chrome..69i57.987j0j1&sourceid=chrome&es_sm=93&ie=UTF-8&filter=0"
#twitter login
#"https://www.google.com/search?q=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&oq=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&num=100&start=100&aqs=chrome..69i57.275j0j1&sourceid=chrome&es_sm=93&ie=UTF-8#q=%22with+twitter%22+inurl:%22%2Flogin%22+-site:twitter.com"


	# for i in range(num_sites/100):
	# 	new_url = "https://www.google.com/search?q=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&oq=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&aqs=chrome..69i57.275j0j1&sourceid=chrome&es_sm=93&ie=UTF-8#q=%22with+twitter%22+inurl:%22%2Flogin%22+-site:twitter.com&num=100&start=" + str(i*100)
	# 	start_urls.append(new_url)

	def parse(self, response):
			for result in response.xpath('//li[@class="g"]'):
				#if "/login&sa=" in str(result.xpath('h3/a/@href').extract()) or "/login/&sa=" in str(result.xpath('h3/a/@href').extract()):
				item = GoogleItem()
				item['title'] = result.xpath('h3/a/text()').extract()
				item['link'] = result.xpath('h3/a/@href').extract()
				#item['desc'] = result.xpath('div/span/text()').extract()
				yield item