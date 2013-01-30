import urllib.request
import re
import datetime
from bs4 import BeautifulSoup

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
page = urllib.request.urlopen(url).read()

#turn page into soup object
soup = BeautifulSoup(page)

#fetch page text
pagetext =(soup.get_text())

#get breakfast lunch and dinner line index
breakfaststart = pagetext.find("BreakfastPenis")
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

#print food
print(breakfast + "\n" + lunch + "\n" + dinner)

print("\n" + url)
