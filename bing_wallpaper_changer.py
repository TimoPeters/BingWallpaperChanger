import requests
import urllib.request
import os


BING_URL = 'https://www.bing.com/'
URL_REGEX = '<div class=\"img_cont\"style=\"background-image: url(/th?id=OHR.FalklandRockhoppers_DE-DE6067934998_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg)\">'
CHANGE_WP_CMD = 'gsettings set org.gnome.desktop.background picture-uri file:///home/timo/Pictures/everaldo-coelho-2tigIl6Tt7E-unsplash.jpg'
WP_DIR_PATH = '/home/$USER/.bing_wallpapers'


def fetch_picture_of_the_day(url):
    urllib.request.urlretrieve(url, "/home/timo/local-filename.jpg")


htmltext = requests.get(BING_URL).text


print(os.path.exists(WP_DIR_PATH))

# Create a directory to safe the pictures in
if not os.path.exists(WP_DIR_PATH):
    os.system(f'mkdir ${WP_DIR_PATH}')
    print('Created dir')


# Change Wallpaper
os.system(CHANGE_WP_CMD)

fetch_picture_of_the_day("https://www.bing.com//th?id=OHR.FalklandRockhoppers_DE-DE6067934998_1920x1080.jpg&rf=LaDigue_1920x1080.jpg")

# ToDo Create Regex
# ToDo Find a way to Download and safe the .jpg in a given directory
# ToDo Automate downloading the newest image in a given interval
# ToDo If the directory is bigger than 500MB -> delete the oldest image
# ToDo Run script on Boot
