"""******************************************************************
 * Displays information about NDSU Lunch menus for various locations*
 * 																	*												*
 * v1.0																*
 *****************************************************************"""

import urllib2
import re
import datetime
import bs4
import wx

def updateMenu(location, dayoffset, meal):
	#create desired page url (from current date and residence dining center by default)
	locnumresidence = "04"
	locnumwest = "02"
	locnumunion = "10"
	if (location == "residence"):
		diningcenter = locnumresidence
	elif (location == "west"):
		diningcenter = locnumwest
	else:
		diningcenter = locnumunion

	now = datetime.datetime.now()
	if (dayoffset >= 0):
		offset = now + datetime.timedelta(days= dayoffset)
	else:
		offset = now - datetime.timedelta(days= (0 - dayoffset))


	daynumber = str(offset.day)
	monthnumber = str(offset.month)
	yearnumber = str(offset.year)

	url = "http://www.ndsu.edu/dining_services/menu/shortmenu.asp?sName=Go+Bison%21&locationNum=" + diningcenter + "&locationName=&naFlag=&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=" + monthnumber + "%2F" + daynumber + "%2F" + yearnumber

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
	if (meal == "breakfast"):
		return breakfast
	elif (meal == "lunch"):
		return lunch
	elif (meal == "dinner"):
		return dinner
	else :
		raise Exception("I dun' goofed.")
		return

class GUI(wx.Frame):

	#default startup values
	weekday = datetime.datetime.now().isoweekday() #returns weekday as integer 1-7 starting with monday
	weekday = weekday + 1 #adjust for sunday as start of week
	if (weekday == 8):
		weekday = 1
	location = "residence"
	meal = "dinner"
	dayoffset = 0

	def ClearLocationBackgroundColors(self):
		self.Residence.SetBackgroundColour('wx.NullColor')
		self.West.SetBackgroundColour('wx.NullColor')
		self.Union.SetBackgroundColour('wx.NullColor')
	def ClearDayBackgroundColors(self):
		self.Sun.SetBackgroundColour('wx.NullColor')
		self.Mon.SetBackgroundColour('wx.NullColor')
		self.Tues.SetBackgroundColour('wx.NullColor')
		self.Wens.SetBackgroundColour('wx.NullColor')
		self.Thurs.SetBackgroundColour('wx.NullColor')
		self.Fri.SetBackgroundColour('wx.NullColor')
		self.Sat.SetBackgroundColour('wx.NullColor')
	def ClearMealBackgroundColors(self):
		self.Breakfast.SetBackgroundColour('wx.NullColor')
		self.Lunch.SetBackgroundColour('wx.NullColor')
		self.Dinner.SetBackgroundColour('wx.NullColor')

	def ResidenceClick(self,event):
		self.location = "residence"
		self.ClearLocationBackgroundColors()
		self.Residence.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def WestClick(self,event):
		self.location = "west"
		self.ClearLocationBackgroundColors()
		self.West.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def UnionClick(self,event):
		self.location = "union"
		self.ClearLocationBackgroundColors()
		self.Union.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)

	def SunClick(self,event):
		self.dayoffset = 1 - self.weekday
		self.ClearDayBackgroundColors()
		self.Sun.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def MonClick(self,event):
		self.dayoffset = 2 - self.weekday
		self.ClearDayBackgroundColors()
		self.Mon.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def TuesClick(self,event):
		self.dayoffset = 3 - self.weekday
		self.ClearDayBackgroundColors()
		self.Tues.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def WensClick(self,event):
		self.dayoffset = 4 - self.weekday
		self.ClearDayBackgroundColors()
		self.Wens.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def ThursClick(self,event):
		self.dayoffset = 5 - self.weekday
		self.ClearDayBackgroundColors()
		self.Thurs.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def FriClick(self,event):
		self.dayoffset = 6 - self.weekday
		self.ClearDayBackgroundColors()
		self.Fri.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def SatClick(self,event):
		self.dayoffset = 7 - self.weekday
		self.ClearDayBackgroundColors()
		self.Sat.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)

	def BreakfastClick(self,event):
		self.meal = "breakfast"
		self.ClearMealBackgroundColors()
		self.Breakfast.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def LunchClick(self,event):
		self.meal = "lunch"
		self.ClearMealBackgroundColors()
		self.Lunch.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)
	def DinnerClick(self,event):
		self.meal = "dinner"
		self.ClearMealBackgroundColors()
		self.Dinner.SetBackgroundColour('#99bbFF')
		self.food.SetLabel(updateMenu(self.location, self.dayoffset, self.meal))
		self.food.CenterOnParent(dir=wx.HORIZONTAL)

	def InitUI(self, frameWidth, frameHeight):

		panel = wx.Panel(self, pos=(0, 0), size=(frameWidth, frameHeight))

		width = (frameWidth / 7) - 0.6
		height = 36

		#Daybuttons
		self.Sun = wx.Button(panel, label='Sunday', pos=(0, 0), size=(width, height))
		self.Sun.Bind(wx.EVT_BUTTON, self.SunClick)
		self.Mon = wx.Button(panel, label='Monday', pos=((width * 1), 0), size=(width, height))
		self.Mon.Bind(wx.EVT_BUTTON, self.MonClick)
		self.Tues = wx.Button(panel, label='Tuesday', pos=((width * 2), 0), size=(width, height))
		self.Tues.Bind(wx.EVT_BUTTON, self.TuesClick)
		self.Wens = wx.Button(panel, label='Wednesday', pos=((width * 3), 0), size=(width, height))
		self.Wens.Bind(wx.EVT_BUTTON, self.WensClick)
		self.Thurs = wx.Button(panel, label='Thursday', pos=((width * 4), 0), size=(width, height))
		self.Thurs.Bind(wx.EVT_BUTTON, self.ThursClick)
		self.Fri = wx.Button(panel, label='Friday', pos=((width * 5), 0), size=(width, height))
		self.Fri.Bind(wx.EVT_BUTTON, self.FriClick)
		self.Sat = wx.Button(panel, label='Saturday', pos=((width * 6), 0), size=(width, height))
		self.Sat.Bind(wx.EVT_BUTTON, self.SatClick)

		height = height * 1.75
		padding = 3

		#Dining Locations
		self.Residence = wx.Button(panel, id=-1, label='Residence', pos=(100, 100), size=(width, height))
		self.Residence.Bind(wx.EVT_BUTTON, self.ResidenceClick)
		self.West = wx.Button(panel, id=-1, label='West', pos=(100, 100 + (height) + padding), size=(width, height))
		self.West.Bind(wx.EVT_BUTTON, self.WestClick)
		self.Union = wx.Button(panel, id=-1, label='Union', pos=(100, 100 + (height * 2) + (padding * 2)), size=(width, height))
		self.Union.Bind(wx.EVT_BUTTON, self.UnionClick)

		#Time
		self.Breakfast = wx.Button(panel, id=-1, label='Breakfast', pos=((frameWidth - width - 6) - 100, 100), size=(width, height))
		self.Breakfast.Bind(wx.EVT_BUTTON, self.BreakfastClick)
		self.Lunch = wx.Button(panel, id=-1, label='Lunch', pos=((frameWidth - width - 6) - 100, 100 + (height) + padding), size=(width, height))
		self.Lunch.Bind(wx.EVT_BUTTON, self.LunchClick)
		self.Dinner = wx.Button(panel, id=-1, label='Dinner', pos=((frameWidth - width - 6) - 100, 100 + (height * 2) + (padding * 2)), size=(width, height))
		self.Dinner.Bind(wx.EVT_BUTTON, self.DinnerClick)

		#Text
		self.food = wx.StaticText(panel, label=updateMenu(self.location, self.dayoffset, self.meal), pos=(0, 0), size=(frameWidth, (frameHeight - 100)), style=wx.ALIGN_CENTRE)
		self.food.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
		self.food.CenterOnParent()

	def __init__(self, parent, title):
		frameWidth = 1024
		frameHeight = 640
		wx.Frame.__init__(self, parent, title=title, style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER, size=(frameWidth,frameHeight))
		self.InitUI(frameWidth, frameHeight)
		self.Center()
		self.Residence.SetBackgroundColour('#99bbFF')
		self.Dinner.SetBackgroundColour('#99bbFF')
		if (GUI.weekday == 1):
			self.Sun.SetBackgroundColour('#99bbFF')
		elif (GUI.weekday == 2):
			self.Mon.SetBackgroundColour('#99bbFF')
		elif (GUI.weekday == 3):
			self.Tues.SetBackgroundColour('#99bbFF')
		elif (GUI.weekday == 4):
			self.Wens.SetBackgroundColour('#99bbFF')
		elif (GUI.weekday == 5):
			self.Thurs.SetBackgroundColour('#99bbFF')
		elif (GUI.weekday == 6):
			self.Fri.SetBackgroundColour('#99bbFF')
		else:
			self.Sat.SetBackgroundColour('#99bbFF')
		self.Show(True)



app = wx.App(False)
frame = GUI(None, 'NDSU Lunch Menu')
app.MainLoop()
