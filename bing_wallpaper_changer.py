import requests
import urllib.request
import os
import getpass
import re

BING_URL = 'https://bing.com'
URL_REGEX = r'.*url\((/th.*\.jpg)'
USER = getpass.getuser()
WP_DIR_PATH = f'/home/{USER}/.bing_wallpapers'

html_text = requests.get(BING_URL).text
oldest_image = ''
newest_image = ''


def fetch_picture_of_the_day(url, image_safe_path):
    urllib.request.urlretrieve(url, image_safe_path)


def create_dir():
    # Create a directory to safe the pictures in
    if not os.path.exists(WP_DIR_PATH):
        os.system('mkdir ' + WP_DIR_PATH)
        print('Created dir')


def set_wallpaper(path):
    print('Path: ' + path)
    os.system(
        f'gsettings set org.gnome.desktop.background picture-uri file://{path}')


def get_image_url(regex, html):
    pattern = re.compile(regex)
    matcher = pattern.findall(html)
    url = 'https://www.bing.com' + matcher[1]
    print(url)
    return url


def get_img_name(url):
    # ToDo Create a regex to filter the image name from the url
    pass


create_dir()
fetch_picture_of_the_day(get_image_url(URL_REGEX, html_text), WP_DIR_PATH + '/newest.jpg')
set_wallpaper(WP_DIR_PATH + '/newest.jpg')


# ToDo Automate downloading the newest image in a given interval
# ToDo If the directory is bigger than 500MB -> delete the oldest image
# ToDo Run script on Boot
