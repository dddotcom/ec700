import scrapy, json, re
from pprint import pprint
from tutorial.items import GoogleItem

class OauthSpider(scrapy.Spider):
	name = "fb_oauth"
	start_urls = []
	with open("check_these_sites.txt", "r") as f:	
		for line in f.read().splitlines():
			start_urls.append(line)
	f.close()
	# print start_urls

	# start_urls = [
	#'https://secure.hulu.com/account/signin',
	# 'https://app.groupme.com/signin'
	#'https://myspace.com/signin',
	#'https://zoom.us/signin',
	#'http://www.buzzfeed.com/signin',
	#'https://www.starbucks.com/account/signin',
	#'https://www.chess.com/login',
	#'http://ask.fm/login',
	#'https://www.internships.com/login',
	# 'https://www.stumbleupon.com/login'
	# ]

	def parse(self, response):
		for result in response.xpath('//div'):
			if "Facebook" in str(result.xpath('span/text()').extract()):
				yield self.saveSite(result.xpath('span/text()').extract(), response.url, "//div/span/text()")
				return
			if "Facebook" in str(result.xpath('a/text()').extract()):
				yield self.saveSite(result.xpath('a/text()').extract(), response.url, "//div/a/text()") 
				return
			
		for result in response.xpath('//button'):
			if "Facebook" in str(result.xpath('p/text()').extract()):
				yield self.saveSite(result.xpath('p/text()').extract(), response.url, "//div/a/text()") 
				return				
			if "Facebook" in str(result.xpath('span/text()').extract()):
				yield self.saveSite(esult.xpath('span/text()').extract(), response.url, "//button/span/text()")
				return
			if "facebook" in str(result.xpath('@provider').extract()):
				yield self.saveSite(result.xpath('@provider').extract(), response.url, "//button/@provider")				
				return
			if "facebook" in str(result.xpath('@data-provider').extract()):
				yield self.saveSite(result.xpath('@data-provider').extract(), response.url, "//button/@data-provider")					
				return

		for result in response.xpath('//a'):						
			if "Facebook" in str(result.xpath('span/text()').extract()):
				yield self.saveSite(result.xpath('span/text()').extract(), response.url, "//a/span/text()")
				return
			if "Facebook" in str(result.xpath('text()').extract()):
				yield self.saveSite(result.xpath('text()').extract(), response.url, "//a/text()")
				return

	def saveSite(self, title, link, desc):
		item = GoogleItem()
		item['title'] = title
		item['link'] = link
		item['desc'] = desc
		return item