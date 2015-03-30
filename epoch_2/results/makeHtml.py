filename = 'google.txt'
html_filename = 'google.html'

html = open(html_filename, 'w')
html.write("<!DOCTYPE html>\n<html>\n<head>" + '\n<!-- Latest compiled and minified CSS --><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">'
	+ '\n<!-- jQuery library --><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>' 
	+ '\n<!-- Latest compiled JavaScript --><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>'
	+ '\n<h1>' + filename + ' Sites</h1></head>\n<body>\n')
html.write('<table class="table table-striped table-bordered table-condensed table-hover">\n\t\t<tr><th>URLs</th></tr>')
with open(filename, "r") as f:	
	for line in f.read().splitlines():
		html_line = '\n\t\t<tr><td><a href="' + line + '">' + line + '</a></td></tr>'
		html.write(html_line)
f.close()

html.write("\n\t</tr>\n</table>\n</body>\n</html>")
html.close()
