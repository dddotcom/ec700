import scrapy
import json
from pprint import pprint
from tutorial.items import GoogleItem

class GoogleSpider(scrapy.Spider):
	name = "google"
	allowed_domains = ["https://www.google.com"]
	num_sites = 100
	start_urls = [
		#"https://www.google.com/search?q=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&oq=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&num=10&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a&channel=fflb"	
		"https://www.google.com/search?q=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&oq=%22with+twitter%22+inurl%3A%22%2Flogin%22+-site%3Atwitter.com&num=" + str(num_sites) +"&aqs=chrome..69i57.275j0j1&sourceid=chrome&es_sm=93&ie=UTF-8#q=%22with+twitter%22+inurl:%22%2Flogin%22+-site:twitter.com"
	]

	def parse(self, response):
			for result in response.xpath('//li[@class="g"]'):
				if "/login&sa=" in str(result.xpath('h3/a/@href').extract()) or "/login/&sa=" in str(result.xpath('h3/a/@href').extract()):
					item = GoogleItem()
					item['title'] = result.xpath('h3/a/text()').extract()
					item['link'] = result.xpath('h3/a/@href').extract()
					#item['desc'] = result.xpath('div/span/text()').extract()
					yield item