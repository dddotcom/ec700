# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#source : http://doc.scrapy.org/en/latest/intro/tutorial.html
class DmozItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
	desc = scrapy.Field()

#source : http://amaral-lab.org/blog/quick-introduction-web-crawling-using-scrapy-part-
class MetacriticItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
	cscore = scrapy.Field()
	uscore = scrapy.Field()
	date = scrapy.Field()
	desc = scrapy.Field()

#my attempt
class FinalFantasyItem(scrapy.Item):
	job = scrapy.Field()
	role = scrapy.Field()
	requirements = scrapy.Field()
	lore = scrapy.Field()
