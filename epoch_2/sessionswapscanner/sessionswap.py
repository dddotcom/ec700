from splinter import Browser
import time
import json
import sys




def find_button(browser, button, href):
	if not button == None:

		btn = browser.find_by_css(button)

		if len(button) == 0:
			print "can't find oauth button"
			return 

	if not href == None:
		btn = browser.find_link_by_href(href)

	return btn

def check_has_state(url, button, href):

	browser = Browser()
	browser.visit(url)
	#browser.fill('user[email]', 'splinter - python acceptance testing for web applications')

	browser.find_by_css

	btn = find_button(browser, button, href)
	
	btn.click()

	#incase it just redirects rather than opens a new window
	if len(browser.windows) == 1:
		if "state=" in browser.windows[0].url or "state%" in browser.windows[0].url:
			browser.quit()
			return True
		else:
			browser.quit()
			return False

	#get the popup window
	popup = browser.windows[1]


	print browser.windows[1].url

	if "state=" in browser.windows[1].url or "state%" in browser.windows[1].url:
		browser.quit()
		return True
	else:
		browser.quit()
		return False


	# button = browser.find_by_name('btnG')


def get_session_cookie(browser):
	cookies = browser.cookies.all()

	if cookies == None:
		return None
	for cookie in cookies:
		if "session" in cookie or  "Session" in cookie or "persistent_id" in cookie or cookie == "id" or cookie == "guid" or "SESSION" in cookie:  
			if not "referrer" in cookie:
				return {cookie: cookies[cookie]}

	return None

#only works with facebook at the moment
def test_session_fixation(signup_url, base_url, button, href):
	browser1 = Browser()
	browser1.visit(signup_url)


	#we use this browser to swap the session
	browser2 = Browser()
	browser2.visit(base_url)


	sessioncookie1 = get_session_cookie(browser1)
	sessioncookie2 = get_session_cookie(browser2)

	browser2.quit()


	#import pdb; pdb.set_trace()

	if sessioncookie1 == None:
		print "sigh, no session cookie might as well give up"
		return

	btn = find_button(browser1, button, href)
	btn.click()


	#import pdb; pdb.set_trace()

	browser1.windows.current = browser1.windows[-1]

	browser1.find_by_id("email").fill("frankzerotwenty@gmx.com")
	browser1.find_by_id("pass").fill("x123457!")


	browser1.windows.current = browser1.windows[0]

	browser1.cookies.delete(sessioncookie1.keys()[0])
	browser1.cookies.add(sessioncookie2)

	browser1.windows.current = browser1.windows[-1]
	time.sleep(2)


	#sign in
	browser1.find_by_id("loginbutton").first.click()

	if len(browser1.windows) == 2:
		browser1.find_by_name("__CONFIRM__").first.click()

	browser1.windows.current = browser1.windows[0]

	browser1.visit(	signup_url )

	return sessioncookie1, sessioncookie2, get_session_cookie(browser1), browser1.windows[0].url, signup_url, base_url



	#print sessioncookie, get_session_cookie(browser2), get_session_cookie(browser1), get_session_cookie(browser2) 
	#browser1.cookies.delete()
	#print sessioncookie, get_session_cookie(browser2), get_session_cookie(browser1), get_session_cookie(browser2) 

	#browser1.quit()
	#browser2.quit()


def test1():
	url = "https://www.goodreads.com/user/sign_up"
	btn = "a.fbButton"
	href = None

	print check_has_state(url, btn, href)

	url = "http://railscasts.com/"
	btn =  None 
	href = "/login?return_to=http%3A%2F%2Frailscasts.com%2F"

	# "a Sign in through GitHub"

	print check_has_state(url, btn, href)

def test2():
	signup_url = "https://www.goodreads.com/user/sign_up"
	base_url = "https://www.goodreads.com"
	btn = "a.fbButton"
	href = None
	#test1()
	print test_session_fixation(signup_url, base_url, btn, href)


def test_session_fixation_smarter(json):
	try:
		browser1 = Browser()

		signup_url = json[u'link'] 
		base_url = signup_url.split("/signin")[0]

		browser1.visit(signup_url)

		#we use this browser to swap the session
		browser2 = Browser()
		browser2.visit(base_url)


		sessioncookie1 = get_session_cookie(browser1)
		sessioncookie2 = get_session_cookie(browser2)

		browser2.quit()


		#import pdb; pdb.set_trace()

		if sessioncookie1 == None:
			print None, "sigh, no session cookie might as well give up"
			print browser1.cookies.all()
			return


		done = False

		ahrefs = browser1.find_by_css("a")

		for element in ["a", "button"]:
			for i in xrange(len(ahrefs)):
				try:
					ahref = browser1.find_by_css(element)[i]

					ahref.click()
					#print browser1.windows.current.url

					if len(browser1.windows) > 1:
						browser1.windows.current = browser1.windows[-1]

					if "facebook.com/log" in browser1.windows.current.url:
						done = True
						break
					else:
						browser1.back()

					if len(browser1.windows) > 1:
						browser1.windows[-1].close()
				except:
					pass

			if done: break

		if not done:
			return None, "failed to find fb button"

		browser1.windows.current = browser1.windows[-1]

		browser1.find_by_id("email").fill("frankzerotwenty@gmx.com")
		browser1.find_by_id("pass").fill("x123457!")


		browser1.windows.current = browser1.windows[0]

		browser1.cookies.delete(sessioncookie1.keys()[0])
		browser1.cookies.add(sessioncookie2)

		browser1.windows.current = browser1.windows[-1]
		time.sleep(2)


		#sign in
		browser1.find_by_id("loginbutton").first.click()

		if len(browser1.windows) == 2:
			browser1.find_by_name("__CONFIRM__").first.click()

		browser1.windows.current = browser1.windows[0]

		browser1.visit(	signup_url )

		output =  sessioncookie1, sessioncookie2, get_session_cookie(browser1), browser1.windows[0].url, signup_url, base_url

		session_cookies_captured = ( sessioncookie1 != sessioncookie2 ) and ( sessioncookie2 == get_session_cookie(browser1) )
		sign_up_success = browser1.windows[0].url == base_url


		browser1.quit()

		if session_cookies_captured:
			return sign_up_success
		else:
			return None
	except:
		return None




pagetoload = int(sys.argv[1])

with open('fb_test.json') as f:    
    json = json.load(f)
    vulnerable = test_session_fixation_smarter(json[pagetoload])

    if vulnerable == None:
    	print "can't tell"
    elif vulnerable == True:
    	print "potentionally vulnerable"
    else: 
    	print "not vulnerable to session swapping"

    # for i in json:
    # 	print i, test_session_fixation_smarter(i)








