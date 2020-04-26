
import requests
from bs4 import BeautifulSoup

BING_URL = 'https://www.bing.com/'
URL_REGEX = '<div class=\"img_cont\"style=\"background-image: url(/th?id=OHR.FalklandRockhoppers_DE-DE6067934998_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg)\">'


htmltext = requests.get(BING_URL).text

print(htmltext)

#ToDo Create Regex
#ToDo Find a way to Download and safe the .jpg in a given directory
#ToDo Find a way to set a Wallpaper
#ToDo Automate downloading the newest image in a given interval
#ToDo If the directory is bigger than 500MB -> delete the oldest image
#ToDo Run script on Boot