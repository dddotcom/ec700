import scrapy
from scrapy.selector import HtmlXPathSelector
from tutorial.items import MetacriticItem

class MetacriticSpider(scrapy.Spider):
	name = "metacritic"
	allowed_comains = ["metacritic.com"]
	start_urls = [
		"http://www.metacritic.com/browse/games/title/pc?page=0"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		sites = hxs.select('//li[contains(@class, "product game_product")]/div[@class="product_wrap"]')
		items = []

		for site in sites:
			item = MetacriticItem()
			item['title'] = site.select('div[@class="basic_stat product_title"]/a/text()').extract()
			items.append(item)
		return items
