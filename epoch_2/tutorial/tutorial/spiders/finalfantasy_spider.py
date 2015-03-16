from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial.items import FinalFantasyItem

class FinalFantasySpider(BaseSpider):
	name = "ff"
	allowed_comains = ["ffxiv.consolegameswiki.com"]
	start_urls = [
		"http://ffxiv.consolegameswiki.com/wiki/Jobs"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		sites = hxs.select('//h2/span[contains(@class, "mw-headline")]')
		items = []

		for site in sites:
			item = FinalFantasyItem()
			item['role'] = site.select('a/text()').extract()
			items.append(item)

		return items