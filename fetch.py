"""******************************************************************
 * Displays information about NDSU Lunch menus for various locations*
 *     																*
 * Carlin Mische													*
 * v1.0																*
 *****************************************************************"""

import urllib2
import re
import datetime
import bs4
import wx

#create desired page url (from current date and residence dining center by default)
locnumresidence = "04"
locnumwest = "02"
locnumunion = "10"
location = locnumresidence

now = datetime.datetime.now()
daynumber = str(now.day)
monthnumber = str(now.month)
yearnumber = str(now.year)

url = "http://www.ndsu.edu/dining_services/menu/shortmenu.asp?sName=Go+Bison%21&locationNum=" + location + "&locationName=&naFlag=&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=" + monthnumber + "%2F" + daynumber + "%2F" + yearnumber

#request page
page = urllib2.urlopen(url).read()

#turn page into soup object
soup = bs4.BeautifulSoup(page)

#fetch page text
pagetext = soup.get_text().encode('ascii','ignore')

#get breakfast lunch and dinner line index
breakfaststart = pagetext.find("Breakfast")
lunchstart = pagetext.find("Lunch")
dinnerstart = pagetext.find("Dinner")
dinnerend = pagetext.find("Food Allergy Disclaimer")

#get breakfast lunch and dinner substrings
rawbreakfast = pagetext[breakfaststart:lunchstart - 1]
rawlunch = pagetext[lunchstart:dinnerstart - 1]
rawdinner = pagetext[dinnerstart:dinnerend - 1]

#remove blanklines from substrings
def parse(rawfood):
	cookedfood = ""
	for line in rawfood.splitlines():
		if not re.match(r'^\s*$', line):
			if (line.find("Recipe Name Is Displayed Here") == -1):
				cookedfood += line + "\n"
	return cookedfood

breakfast = parse(rawbreakfast)
lunch = parse(rawlunch)
dinner = parse(rawdinner)

class MyFrame(wx.Frame):

	def MonClick(self,event):
		print("Monday")

	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(1000,650))
		self.Center()
		self.Show(True)

		self.Mon = wx.Button(self, id=-1, label='Mon',
			pos=(8, 8), size=(175, 28))
		self.Mon.Bind(wx.EVT_BUTTON, self.MonClick)
		# optional tooltip
		self.Mon.SetToolTip(wx.ToolTip("click to hide"))

	 

app = wx.App(False)
frame = MyFrame(None, 'NDSU Lunch Menu')
app.MainLoop()
