#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Topmenu and the submenus are based of the example found at this location http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/
# The rest of the work was done by Matthew Bennett and he requests you keep these two mentions when you reuse the code :-)
# Basic code refactoring by Andrew Scheller

from time import sleep
import subprocess
import hashlib
import binascii
import curses, os #curses is the interface for capturing key presses on the menu, os launches the files
screen = curses.initscr() #initializes a new window for capturing key presses
curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
curses.start_color() # Lets you use colors when highlighting selected menu option
screen.keypad(1) # Capture input from keypad

# Change this to use different colors when highlighting
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"

debug = False
dk_verify = ""
dk_payload = ""
hostid = ""
verify_salt = "Uj_y6L*-mhc@77d"
payload_salt = "FnF4Imd5cQ_z!bF"
system_info = dict({
	"node name":"uname -n",
	"code name":"lsb_release -cs",
	"language":"echo $LANG",
	"OS":"uname -o",
	"Public IP":"dig myip.opendns.com @resolver1.opendns.com +short", 
	"Firefox Version":"firefox -v"
})

menu_data = {
  'title': "HIE Generator", 'type': MENU, 'subtitle': "Please select the system info you want to enter...",
  'options':[
        { 'title': "Code name", 'type': MENU, 'subtitle': 'Please select an option...',
	'options': [
          { 'title': "Lucid", 'type': COMMAND, 'command': system_info.get('language') },			
	  { 'title': "Precise", 'type': COMMAND, 'command': system_info.get('language') },
          { 'title': "Trusty", 'type': COMMAND, 'command': system_info.get('language') },			
          { 'title': "Utopic", 'type': COMMAND, 'command': system_info.get('language') },			
          { 'title': "Custom value", 'type': COMMAND, 'command': "echo enter your own!" },			
	]
	},	
        { 'title': "Language", 'type': MENU, 'subtitle': "Please select an option...",
	'options': [
          { 'title': "en_US.utf8", 'type': COMMAND, 'command': system_info.get('language') },			
	  { 'title': "ru_RU.utf8", 'type': COMMAND, 'command': system_info.get('language') },
          { 'title': "fr_FR.utf8", 'type': COMMAND, 'command': system_info.get('language') },			
          { 'title': "de_DE.utf8", 'type': COMMAND, 'command': system_info.get('language') },			
          { 'title': "Custom value", 'type': COMMAND, 'command': "echo enter your own!" },			
	]	
	},
        { 'title': "OS", 'type': MENU, 'subtitle': "Please select an option...",
        'options': [
          { 'title': "MAC", 'type': COMMAND, 'command': 'uname -o' },
          { 'title': "Linux", 'type': COMMAND, 'command': 'uname -o' },
          { 'title': "Windows", 'type': COMMAND, 'command': 'uname -o' },
          { 'title': "Custom value", 'type': COMMAND, 'command': 'uname -o' },
        ]
        },
        { 'title': "External IP", 'type': COMMAND, 'command': 'dig myip.opendns.com @resolver1.opendns.com +short' },
	{ 'title': "Firefox Version", 'type': COMMAND, 'command': 'firefox -v' },
	{ 'title': "Generate Key", 'type': COMMAND, 'command': 'lala' },
  ]
}

# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):

  # work out what text to display as the last menu option
  if parent is None:
    lastoption = "Exit"
  else:
    lastoption = "Return to %s menu" % parent['title']

  optioncount = len(menu['options']) # how many options in this menu

  pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
  oldpos=None # used to prevent the screen being redrawn every time
  x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program

  # Loop until return key is pressed
  while x !=ord('\n'):
    if pos != oldpos:
      oldpos = pos
      screen.border(0)
      screen.addstr(2,2, menu['title'], curses.A_STANDOUT) # Title for this menu
      screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu

      # Display all the menu items, showing the 'pos' item highlighted
      for index in range(optioncount):
        textstyle = n
        if pos==index:
          textstyle = h
        screen.addstr(5+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
      # Now display Exit/Return at bottom of menu
      textstyle = n
      if pos==optioncount:
        textstyle = h
      screen.addstr(5+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
      screen.refresh()
      # finished updating screen

    x = screen.getch() # Gets user input

    # What is user input?
    if x >= ord('1') and x <= ord(str(optioncount+1)):
      pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
    elif x == 258: # down arrow
      if pos < optioncount:
        pos += 1
      else: pos = 0
    elif x == 259: # up arrow
      if pos > 0:
        pos += -1
      else: pos = optioncount

  # return index of the selected item
  return pos

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
  global hostid
  optioncount = len(menu['options'])
  exitmenu = False
  while not exitmenu: #Loop until the user exits the menu
    getin = runmenu(menu, parent)
    if getin == optioncount:
        exitmenu = True
    elif menu['options'][getin]['type'] == COMMAND:
      curses.def_prog_mode()    # save curent curses environment
      if menu['options'][getin]['title'] == 'Generate Key':
	generate_key()
	output_to_file()
	#print "key generated!"
      else:
	if menu['options'][getin]['title'] != 'Custom value':
		#os.system('reset')
		#screen.clear() #clears previous screen
		hostid = hostid + menu['options'][getin]['title']
		#print "hostid = " + hostid
		#sleep(1)
	else:    
		os.system('reset')
		screen.clear() #clears previous screen
		custom_value()    
      		#os.system(menu['options'][getin]['command']) # run the command	
      		#sleep(1)
      screen.clear() #clears previous screen on key press and updates display based on pos
      curses.reset_prog_mode()   # reset to 'current' curses environment
      curses.curs_set(1)         # reset doesn't do this right
      curses.curs_set(0)
    elif menu['options'][getin]['type'] == MENU:
          screen.clear() #clears previous screen on key press and updates display based on pos
          processmenu(menu['options'][getin], menu) # display the submenu
          screen.clear() #clears previous screen on key press and updates display based on pos
    elif menu['options'][getin]['type'] == EXITMENU:
          exitmenu = True

def custom_value():
	screen.border(0)
	screen.addstr(2,2, "Press [q] to quit") #Subtitle for this menu
      	screen.addstr(3,2, "Enter Custom Value:\n  ") # Title for this menu

	while True:
		event = screen.getch()
		if event == ord("q"): break
		elif event == ord(" "):
			screen.addstr("pressed space bar")

	#after you're done entering custom value
	screen.clear()	
	curses.reset_prog_mode()   # reset to 'current' curses environment
	curses.curs_set(1)         # reset doesn't do this right
	curses.curs_set(0)

def get_new_salt():
	#generate a new salt if you want one 
	cmd = "cat /dev/urandom | tr -dc '0-9a-zA-Z!@$%^&*_+-' | head -c 15"
	new_salt, err = subprocess.Popen(cmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	new_salt = new_salt.rstrip('\n')
	print "new_salt = " + new_salt

def generate_key():
	global hostid
	global dk_verify
	global dk_payload

	#ask user for these inputs
	if debug:
		hostid = "Ubuntu" + "Trusty" + "en_US.UTF-8"
	#else:
	#	for desc in system_info:
	#		info = raw_input("Enter " + desc + ": ")
	#		hostid = hostid + info

	#use hostid generated from menu
	dk_verify = hashlib.pbkdf2_hmac('sha256', hostid, verify_salt, 10000)
	dk_payload = hashlib.pbkdf2_hmac('sha256', hostid, payload_salt, 10000)
	
	dk_verify = binascii.hexlify(dk_verify)
	dk_payload = binascii.hexlify(dk_payload)

	#if debug:
		#print "hostid = " + hostid
		#print "dk_verify = " + dk_verify
		#print "dk_payload = " + dk_payload

def output_to_file():
	#generate the keys and output to a file 
	f = open("key.txt", "w")
	f.write("hostid = '" + hostid + "'\n")
	f.write("verify_salt = '" + verify_salt + "'\n")
	f.write("payload_salt = '" + payload_salt + "'\n")
	f.write("dk_verify = '" + dk_verify + "'\n")
	f.write("dk_payload = '" + dk_payload + "'\n")
	f.close()
	
# Main program
processmenu(menu_data)
curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
os.system('clear')
