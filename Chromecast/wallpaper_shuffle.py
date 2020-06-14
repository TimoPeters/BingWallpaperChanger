import random
import os
import time

PATH = '/home/timo/Pictures/chromecast_wallpapers'

while True:
    rand_file = random.choice(os.listdir(PATH))
    rand_path = PATH + '/' + rand_file
    os.system(
        f'gsettings set org.gnome.desktop.background picture-uri file://{rand_path}')
    print('Set new Wallpaper: ' + rand_path)
    time.sleep(15 * 60)
