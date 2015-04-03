#
# Open up a webpage and look at how the page changes when we
# automatically sign into Facebook using the client flow.
# 
# If the client flow is not available, we simply quit.
# 
#
 
import re

from splinter.browser import Browser
from bs4 import BeautifulSoup

from selenium.common.exceptions import WebDriverException
from pprint import pprint
from time import sleep

verbose = False

browser = Browser()

# TODO: get url from file
url = 'https://www.goodreads.com/user/sign_in?source=home'

browser.visit(url)

# Add in Javascript to intercept various interactions.

with open("client.js", "r") as file:
	interceptjs = file.read()

browser.execute_script(interceptjs)

# Rip out the html from the browser and query it for elements
# of interest
html = browser.evaluate_script('document.body.innerHTML')

soup = BeautifulSoup(html)

links = soup.find_all('a')

bs = soup.find_all('button')

candidates = ['^fb.*', '.*fb$', '.*facebook.*']

regex = '|'.join(candidates)

found = False

for a in links:
    if a['href'] == "#":
        classes = a['class']
	for cls in classes:
		if re.match(regex, cls, re.IGNORECASE):
			found = True	
			break
	if found:
		break	
if found:
	print "Found the Facebook button!"
	btn = browser.find_by_css('.'+cls)
	btn.click()
else:
	print "Could not find Facebook button, closing browser now..."
	browser.quit()
  	exit()

win = browser.windows[0]
popup = browser.windows[-1]

browser.windows.current = popup

browser.fill('email', 'frankzerotwenty@gmx.com')
browser.fill('pass', 'x123457!')

browser.find_by_name('login').click()

# Give as many permissions as we need to this app
while True:
	try:
		confirm = browser.find_by_name('__CONFIRM__')
		if not confirm:
			break
		else:
			confirm.click()
	except WebDriverException:
		# It's tough to tell exactly when a window has
		# closed.
		break

browser.windows.current = win

# Wait a few seconds and see if the page tries to
# go anywhere. Our beforeunload event will stop
# it
sleep(3)

with browser.get_alert() as alert:
	if alert:
		alert.dismiss()

# Get the new cookies
browser.execute_script("window.KO.cookies1 = window.KO.getcookies();")

# Retrieve our state that has everything
KO = browser.evaluate_script("window.KO")

# Search for an Access Token
pairs = KO['data'].split('&')

for kv in pairs:
	k, v = kv.split('=')
	if k == 'access_token':
		print "Access Token Found:"
		print v

# Find cookies that were changed by logging in
print "The following cookies' values were changed by logging in:"
for k in KO['cookies0']:
	if k not in KO['cookies1']:
		print "Cookie ", k, " was deleted."
		continue

	old = KO['cookies0'][k]
	new = KO['cookies1'][k]
	if old != new:
		print "Cookie ", k ,":", old , " --> ", new

print ""

oldcookies = set(k for k in KO['cookies0'])
newcookies = set(k for k in KO['cookies1'])

diffcookies = newcookies - oldcookies  

print "The following cookies were added or deleted by logging in:"

for k in diffcookies:
	
	if k not in KO['cookies1']:
		value = KO['cookies0'][k]
	else:
		value = KO['cookies1'][k]
	print "Cookie ", k, ": ", KO['cookies1'][k]

print ""

# Display any AJAX information if it was recorded
ajax = KO['ajaxhistory']

for req in ajax:
	method = req['method']
	url = req['url']
	data = req['data']

	print method, " ", url, ":"
	print "data:", data
	print ""


# Display all the data in one big object
if verbose:
	print "Dumping All KillOAuth Data:"
	pprint(KO)

browser.quit()
