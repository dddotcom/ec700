#!/bin/bash 
#empty files first
> out.json
> check_these_sites.txt
> oauth_sites.json
> final_check_these_sites.txt

echo "starting google search..."
scrapy crawl google -o out.json 2>&1
echo "retreiving valid login urls..."
python -c'import parse_urls; parse_urls.find_login_pages()'
echo "starting oauth scraper..."
scrapy crawl oauth -o oauth_sites.json 2>&1 
echo "generating list of unique URLS to try!"
python -c'import parse_urls; parse_urls.generate_unique_url_list()'
echo "done!"
