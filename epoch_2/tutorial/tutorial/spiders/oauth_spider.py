import scrapy, json, re
from pprint import pprint
from tutorial.items import GoogleItem

class OauthSpider(scrapy.Spider):
	name = "oauth"
	start_urls = []
	with open("check_these_sites.txt", "r") as f:	
		for line in f.read().splitlines():
			start_urls.append(line)
	f.close()
	print start_urls

	# start_urls = [
	# 	'https://www.pinterest.com/login/',
	# 	'https://hootsuite.com/login',
	# 	'http://ask.fm/login'
	# 	]

	def find_login_pages():
		with open('out.json') as data_file:    
		    data = json.load(data_file)
		for d in data:
			if "/login&sa=" in str(d["link"]) or "/login/&sa=" in str(d["link"]):
				#pprint(d["title"])
				#search through url
				#pprint(str(d["link"]).split("/url?q=")[1])	
				start_urls.append(re.search("(?P<url>https?://[^\s]+)", str(d["link"])).group("url").split("&sa=")[0])

	def parse(self, response):

		# for result in response.xpath('//li[@class="g"]'):
		for result in response.xpath('//button'):
			if "with Twitter" in str(result.xpath('span/text()').extract()):
				item = GoogleItem()
				item['title'] = result.xpath('span/text()').extract()
				item['link'] = response.url
				item['desc'] = "//button/span/text()"
				yield item
			if "twitter" in str(result.xpath('@provider').extract()):
				item = GoogleItem()
				item['title'] = result.xpath('@provider').extract()
				item['link'] = response.url
				item['desc'] = "//button/@provider"
				yield item

		for result in response.xpath('//a'):
			if "with Twitter" in str(result.xpath('span/text()').extract()):
				item = GoogleItem()
				item['title'] = result.xpath('span/text()').extract()
				item['link'] = response.url
				item['desc'] = "//a/span/text()"
				yield item
			if "Twitter" in str(result.xpath('text()').extract()):
				item = GoogleItem()
				item['title'] = result.xpath('text()').extract()
				item['link'] = response.url
				item['desc'] = "//a/text()"
				yield item
			if "twitter" in str(result.xpath('@href').extract()):
				item = GoogleItem()
				item['title'] = result.xpath('@href').extract()
				item['link'] = response.url
				item['desc'] = "//a/@href"
				yield item
