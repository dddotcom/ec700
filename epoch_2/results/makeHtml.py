import json

json_file = 'oauth_sites.json'

def generate_html(filename):
	#get unique urls
	unique_urls = set()
	with open(filename + '.json') as data_file:    
	    data = json.load(data_file)
	for d in data:
		unique_urls.add(str(d["link"]))
	total = len(unique_urls)

	html = open(filename + '.html', 'w')
	html.write("<!DOCTYPE html>\n<html>\n<head>" + '\n<!-- Latest compiled and minified CSS --><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">'
		+ '\n<!-- jQuery library --><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>' 
		+ '\n<!-- Latest compiled JavaScript --><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>'
		+ '</head>\n<body>\n<div class="container">\n<h1>' + filename + ' Sites (' + str(total) +')</h1>')
	html.write('<table class="table table-striped table-bordered table-condensed table-hover">\n\t\t<tr><th> </th><th>URLs</th></tr>')

	url_id = 0
	for url in unique_urls:
			url_id +=1
			html_line = '\n\t\t<tr><td>'+ str(url_id) + '</td><td><a href="' + url + '">' + url + '</a></td></tr>'
			html.write(html_line)

	html.write("\n\t</tr>\n</table>\n</div>\n</body>\n</html>")
	html.close()
