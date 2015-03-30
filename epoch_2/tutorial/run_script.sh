#!/bin/bash 


#echo "starting google search..."
#> out.json
#scrapy crawl google -o out.json 2>&1

echo "retreiving valid login urls..."
> check_these_sites.txt
python -c'import parse_urls; parse_urls.find_login_pages("google")'

echo "starting oauth scraper..."
> oauth_sites.json
scrapy crawl googleOauth -o oauth_sites.json 2>&1 
#scrapy crawl facebook -o oauth_sites.json 2>&1 

echo "generating list of unique URLS to try!"
> final_check_these_sites.txt
python -c'import parse_urls; parse_urls.generate_unique_url_list()'
echo "done!"
