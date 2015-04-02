#!/bin/bash 

if [ $# -eq 1 ] && [ $1 == "--help" ]; then
	echo -e "Usage:\n  ./run_script.sh <idp_name> <spider_name> [output_file]\n"
	echo -e "Outputs:\n [output_file].json   Contains verified Oauth URLs in JSON format\n [output_file].html   Contains verified Oauth URLs in a visual HTML table format\n [output_file].log    Contains scrapy log of spider used\n"
	echo -e "Run this script with any of the following commands:"
	echo -e "  (1)./run_script.sh twitter tw_oauth [output_file]"
	echo -e "  (2)./run_script.sh facebook fb_oauth [output_file]"
	echo -e "  (3)./run_script.sh google go_oauth [output_file]\n"
	echo -e "    <idp_name>=Identity Provider Name\n    List of all possible idp names:"
	echo -e "      (1)twitter  (2)facebook  (3)google\n"
	echo -e "    <spider_name>=Web Crawler Name\n    List of all possible spiders:"
	echo -e "      (1)tw_oauth  (2)fb_oauth  (3)go_oauth\n"
elif [ $# -eq 0 ] || [ $# -eq 1 ] || [ $# -eq 2 ]; then
	echo -e "Error: Not enough arguments."
	echo -e 'Use "./run_script.sh --help" to view options'
else
	# if [ "$1" != "google" ]; then 
	if [ "$1" != "google" ] && [ "$1" != "twitter" ] && [ "$1" != "facebook" ]; then 
		echo -e "Error: <idp_name> not recognized."
		echo -e "Usage:\n  ./run_script.sh <idp_name> <spider_name> [output_file]\n"
		echo -e "List of all possible idp names:"
		echo -e "(1)twitter  (2)facebook  (3)google\n"
	elif [ "$2" != "go_oauth" ] && [ "$2" != "tw_oauth" ] && [ "$2" != "fb_oauth" ]; then  
		echo -e "Error: <spider_name> not recognized."
		echo -e "Usage:\n  ./run_script.sh <idp_name> <spider_name> [output_file]\n"
		echo -e "List of all possible spiders:"
		echo -e "(1)tw_oauth  (2)fb_oauth  (3)go_oauth\n"
	else
		# echo "starting google search..."
		# > out.json
		# scrapy crawl google -o out.json 2>&1

		# echo "Retrieving valid $1 login urls..."
		# > check_these_sites.txt
		# python -c"import parse_urls; parse_urls.find_login_pages('$1')"

		 # echo "Starting oauth scraper: $2..."
		 # #> ../results/oauth_sites.json
		 # scrapy crawl $2 -o ../results/$3.json --logfile=../results/$3.log &
		 # pid=$!
		 # while kill -0 $pid 2> /dev/null; do
		 # 	echo -ne "."
		 # 	sleep 0.5
		 # done

		echo -ne "\nGenerating output of verified URLS..."
		cd ../results
		python -c"import makeHtml; makeHtml.generate_html('$3')"
		echo -ne "\nDONE!\nVerified URLs can be found at $3.html and $3.json\nLog file can be found at $3.log\n"
	fi
fi


