import requests
import urllib.request
import glob
import os
from pathlib import Path
import getpass
import re
import time
import json

with open('settings.json') as file:
    settings = json.load(file)

BING_URL = 'https://bing.com'
URL_REGEX = r'.*url\((/th.*\.jpg)'  # Regex to get the image URL from the html
USER = getpass.getuser()
WP_DIR_PATH = f'/home/{USER}/.bing_wallpapers'
REFRESH_INTERVAL = settings['refresh_interval'] * 60  # The refresh interval in seconds
MAX_DIR_SIZE = settings['max_dir_size'] * 1000000  # The maximum size the dir can have in bytes


def fetch_picture_of_the_day(url, image_safe_path):
    # Safes the new bing picture of the day in the .bing_wallpaper directory
    urllib.request.urlretrieve(url, f'{image_safe_path}')
    print(f'Fetched new image: {image_name}')


def create_dir():
    # Create a directory to safe the pictures in
    if not os.path.exists(WP_DIR_PATH):
        print(f'{WP_DIR_PATH} does not exist')
        os.system(f'mkdir {WP_DIR_PATH}')
        print(f'Created dir: {WP_DIR_PATH}')


def set_wallpaper(path):
    # Set the Wallpaper
    print('Set new Wallpaper: ' + path)
    os.system(
        f'gsettings set org.gnome.desktop.background picture-uri file://{path}')


def get_image_url(regex, html):
    # Filters the image URL from the fetched Bing html
    pattern = re.compile(regex)
    matcher = pattern.findall(html)
    url = 'https://www.bing.com' + matcher[1]
    return url


def get_img_name(url):
    # Filter the image name from the URL
    pattern = re.compile(r'\/th\?id=OHR\.(.*)_[A-Z]{2}.*')
    matcher = pattern.findall(url)
    return matcher[0] + '.jpg'


def get_newest_img(dir_path):
    # Returns the newest file in the directory
    list_of_files = glob.glob(dir_path + '/*')
    if not len(list_of_files) <= 0:
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file


def remove_oldest_img(dir_path):
    # Removes the oldest file from the directory
    list_of_files = glob.glob(dir_path + '/*')
    latest_file = min(list_of_files, key=os.path.getctime)
    os.remove(latest_file)
    print(f'Removed: {latest_file}')


def calc_dir_size(dir_path):
    # Returns the combined size a given directory
    wp_dir = Path(dir_path)
    return sum(f.stat().st_size for f in wp_dir.glob('**/*') if f.is_file())


while True:
    # Request the bing html and filter the image URL and image name
    print(f'Requesting data from {BING_URL}')
    html_text = requests.get(BING_URL).text
    image_url = get_image_url(URL_REGEX, html_text)
    image_name = get_img_name(image_url)

    # Create the .bing_wallpapers directory if it doesn't exist
    create_dir()
    # If a new image is found -> safe the image and set it as wallpaper
    if not os.path.exists(f'{WP_DIR_PATH}/{image_name}'):
        fetch_picture_of_the_day(image_url, f'{WP_DIR_PATH}/{image_name}')
        newest_image = get_newest_img(WP_DIR_PATH)
        set_wallpaper(newest_image)
    else:
        print('No new image found')

    # If the .bing_wallpapers directory exceeds the max directory size -> remove the oldest file
    if calc_dir_size(WP_DIR_PATH) > MAX_DIR_SIZE:
        remove_oldest_img(WP_DIR_PATH)

    # Sleep for a given time and start the routine over again
    time.sleep(REFRESH_INTERVAL)
