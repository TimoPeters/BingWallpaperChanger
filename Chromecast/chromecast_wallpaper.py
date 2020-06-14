import requests as req
import os
import urllib.request
import re
import random
import string

WP_DIR_PATH = '/home/timo/Pictures/chromecast_wallpapers'
JSON_URL = 'https://chromecastbg.alexmeub.com/images.v9.json'
images_json = req.get(JSON_URL).json()


def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def config_url(url):
    # ToDo: https://lh4.googleusercontent.com/-9VBXTbvWld0/U_yjmbN6zVI/AAAAAAAB-3c/rSgR3kL3uTQ/s2560/20101103_TorresDelPaine_Cuernos_Horns_6215_blended-Edit-Edit-Edit.jpg
    regex = '.*(s[0-9]*-w[0-9]*-h[0-9]*).*'
    alt_regex = '.*\/(s[0-9]*)\/.*'
    pattern = re.compile(regex)
    alt_pattern = re.compile(alt_regex)
    matcher = pattern.findall(url)
    alt_matcher = alt_pattern.findall(url)
    if len(matcher) > 0:
        print('REGULAR REGEX')
        url = url.replace(matcher[0], 's1920-w1920-h1080')
    elif len(alt_matcher) > 0:
        print('ALT REGEX')
        url = url.replace(alt_matcher[0], 's2560')
    else:
        print('No REGEX matching')

    return url


# Step1: Create directory to safe the images in
if not os.path.exists(WP_DIR_PATH):
    print(f'{WP_DIR_PATH} does not exist')
    os.system(f'mkdir {WP_DIR_PATH}')
    print(f'Created dir: {WP_DIR_PATH}')

# Step2: Loop over URL's, configure them and safe the images
for data in images_json:
    url = config_url(data['url'])
    try:
        status_code = req.get(url).status_code
    except:
        print('HTTP GET FAILED')

    if status_code is not 200:
        print('Requesting: ', url)
        print('Status Code is ', status_code, ' instead of 200')
    else:
        print('Requesting: ', url)
        print('Status Code is 200')
        # ToDo No random name is generated or the condition does not go through
        if len(data['name']) > 0:
            urllib.request.urlretrieve(url, f'{WP_DIR_PATH}/{data["name"]}')
            print('Saved image: ', data['name'], 'at ', WP_DIR_PATH)
        else:
            name = 'IMG_' + random_string() + '.jpg'
            urllib.request.urlretrieve(url, f'{WP_DIR_PATH}/{name}')
            print('Saved image: ', name, 'at ', WP_DIR_PATH)

