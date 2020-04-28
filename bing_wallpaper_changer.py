import requests
import urllib.request
import glob
import os
from pathlib import Path
import getpass
import re
import time

BING_URL = 'https://bing.com'
URL_REGEX = r'.*url\((/th.*\.jpg)'
USER = getpass.getuser()
WP_DIR_PATH = f'/home/{USER}/.bing_wallpapers'
REFRESH_INTERVAL = 300000


def fetch_picture_of_the_day(url, image_safe_path):
    urllib.request.urlretrieve(url, f'{image_safe_path}')
    print(f'Fetched new image: {image_name}')


def create_dir():
    # Create a directory to safe the pictures in
    if not os.path.exists(WP_DIR_PATH):
        os.system('mkdir ' + WP_DIR_PATH)
        print('Created dir: ' + WP_DIR_PATH)


def set_wallpaper(path):
    print('Set new Wallpaper: ' + path)
    os.system(
        f'gsettings set org.gnome.desktop.background picture-uri file://{path}')


def get_image_url(regex, html):
    pattern = re.compile(regex)
    matcher = pattern.findall(html)
    url = 'https://www.bing.com' + matcher[1]
    return url


def get_img_name(url):
    pattern = re.compile(r'\/th\?id=OHR\.(.*)_DE.*')
    matcher = pattern.findall(url)
    return matcher[0] + '.jpg'


def get_newest_img(dir_path):
    list_of_files = glob.glob(dir_path + '/*')
    if not len(list_of_files) <= 0:
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file


def remove_oldest_img(dir_path):
    list_of_files = glob.glob(dir_path + '/*')
    latest_file = min(list_of_files, key=os.path.getctime)
    os.remove(latest_file)
    print(f'Removed: {latest_file}')


def calc_dir_size(dir_path):
    wp_dir = Path(dir_path)
    return sum(f.stat().st_size for f in wp_dir.glob('**/*') if f.is_file())


while True:
    print(f'Requesting data from {BING_URL}')
    html_text = requests.get(BING_URL).text
    image_url = get_image_url(URL_REGEX, html_text)
    image_name = get_img_name(image_url)

    create_dir()
    if not os.path.exists(f'{WP_DIR_PATH}/{image_name}'):
        fetch_picture_of_the_day(image_url, f'{WP_DIR_PATH}/{image_name}')
        newest_image = get_newest_img(WP_DIR_PATH)
        set_wallpaper(newest_image)
    else:
        print('No new image found')

    if calc_dir_size(WP_DIR_PATH) > 500000000:
        remove_oldest_img(WP_DIR_PATH)

    time.sleep(30.0)

# ToDo Move Settings to a .json
# ToDo Run script on Boot
