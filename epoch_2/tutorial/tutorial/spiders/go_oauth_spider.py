import scrapy, json, re
from pprint import pprint
from tutorial.items import GoogleItem

class OauthSpider(scrapy.Spider):
	name = "go_oauth"
	start_urls = []
	with open("check_these_sites.txt", "r") as f:	
		for line in f.read().splitlines():
			start_urls.append(line)
	f.close()
	# print start_urls

	# start_urls = [
	# 'https://www.buzzmath.com/signin',
	# 'http://badoo.com/signin/',
	# 'https://todaysmeet.com/accounts/signin',
	# 'https://www.pivotaltracker.com/signin',
	# 'https://www.caringbridge.org/signin',
	# 'https://www.pinterest.com/login/',
	# 'https://www.khanacademy.org/login',
	# 'https://getpocket.com/login',
	# 'https://www.blendspace.com/login',
	# 'https://zoom.us/signin'
	# ]

	def parse(self, response):
		for result in response.xpath('//div'):
			if "Google" in str(result.xpath('span/text()').extract()):
				yield self.saveSite(result.xpath('span/text()').extract(), response.url, "//div/span/text()")
				return
			if "Google" in str(result.xpath('a/text()').extract()):
				yield self.saveSite(result.xpath('a/text()').extract(), response.url, "//div/a/text()") 
				return
			
		for result in response.xpath('//button'):
			if "with Google" in str(result.xpath('text()').extract()):
				yield self.saveSite(result.xpath('p/text()').extract(), response.url, "//div/a/text()") 
				return					
			if "Google" in str(result.xpath('p/text()').extract()):
				yield self.saveSite(result.xpath('p/text()').extract(), response.url, "//div/a/text()") 
				return				
			if "with Google" in str(result.xpath('span/text()').extract()):
				yield self.saveSite(result.xpath('span/text()').extract(), response.url, "//button/span/text()")
				return
			if "google" in str(result.xpath('@provider').extract()):
				yield self.saveSite(result.xpath('@provider').extract(), response.url, "//button/@provider")				
				return
			if "google" in str(result.xpath('@data-provider').extract()):
				yield self.saveSite(result.xpath('@data-provider').extract(), response.url, "//button/@data-provider")					
				return

		for result in response.xpath('//a'):						
			if "Google" in str(result.xpath('span/text()').extract()):
				yield self.saveSite(result.xpath('span/text()').extract(), response.url, "//a/span/text()")
				return
			if "Google" in str(result.xpath('text()').extract()):
				yield self.saveSite(result.xpath('text()').extract(), response.url, "//a/text()")
				return
			if "google" in str(result.xpath('@href').extract()):
				yield self.saveSite(result.xpath('@href').extract(), response.url, "//a/@href")
				return

	def saveSite(self, title, link, desc):
		item = GoogleItem()
		item['title'] = title
		item['link'] = link
		item['desc'] = desc
		return item