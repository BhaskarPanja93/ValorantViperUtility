try:
    from PIL import Image
    from requests import get
    from pyautogui import locateOnScreen, size
    from tkinter import Tk, Label
except:
    import pip
    pip.main(['install', 'pyautogui'])
    pip.main(['install', 'tkinter'])
    pip.main(['install', 'opencv_python'])
    pip.main(['install', 'pillow'])
    pip.main(['install', 'requests'])
    del pip

from tempfile import gettempdir
from tkinter import Tk, Label
from time import sleep
from threading import Thread
from pyautogui import locateOnScreen, size
from os import system as system_caller
from PIL import Image
from requests import get

fps = 10
map_name = None
molly_label = None
smoke_label = None
screen_res = size()
dist_molly = dist_smoke = last_molly_dist = last_smoke_dist = last_y = '-'

sky_region_above = (int(0.491 * screen_res[0]), 0, int(0.0162 * screen_res[0]), int(0.03 * screen_res[1]))
sky_region_below = (int(0.491 * screen_res[0]), int(0.056 * screen_res[1]), int(0.016 * screen_res[0]), int(0.38333 * screen_res[1]))

all_images = {}
extension = '.PNG'
maps = {'1': 'Ascent', '2': 'Bind', '3': 'Breeze', '4': 'Haven', '5': 'Icebox', '6': 'Split'}


def dist_calculator(y):
    if y == '-':
        smoke_dist = molly_dist = y
        update_displayed_values(molly_dist=molly_dist, y=y, smoke_dist=smoke_dist)
    else:
        molly_dist = smoke_dist = '-'
        pixel_count = y
        if pixel_count in molly_1080p:
            molly_dist = molly_1080p[pixel_count]
        if pixel_count in smoke_1080p:
            smoke_dist = smoke_1080p[pixel_count]
        update_displayed_values(molly_dist=molly_dist, smoke_dist=smoke_dist, y=y)


def create_molly_overlay():
    global molly_label
    molly_label = Tk()
    molly_label = Label(molly_label, text='-', font=('Libre Bodoni', '10'), fg='black', bg='red')
    molly_label.master.overrideredirect(True)
    molly_label.master.geometry("+1000-0")
    molly_label.master.wm_attributes("-topmost", True)
    molly_label.master.wm_attributes("-disabled", True)
    molly_label.master.wm_attributes("-transparentcolor", "white")
    molly_label.pack()
    molly_label.mainloop()


def create_smoke_overlay():
    global smoke_label
    smoke_label = Tk()
    smoke_label = Label(smoke_label, text='-', font=('Libre Bodoni', '10'), fg='black', bg='red')
    smoke_label.master.overrideredirect(True)
    smoke_label.master.geometry("-1000-0")
    smoke_label.master.wm_attributes("-topmost", True)
    smoke_label.master.wm_attributes("-disabled", True)
    smoke_label.master.wm_attributes("-transparentcolor", "white")
    smoke_label.pack()
    smoke_label.mainloop()


def update_displayed_values(y, molly_dist=None, smoke_dist=None):
    global last_y, last_smoke_dist, last_molly_dist
    if last_y != y:
        if molly_dist and molly_dist != last_molly_dist:
            molly_label.config(text=molly_dist)
            last_molly_dist = molly_dist
        if smoke_dist and smoke_dist != last_smoke_dist:
            smoke_label.config(text=smoke_dist)
            last_smoke_dist = smoke_dist
        last_y = y


def pixel_finder():
    global map_name, all_images
    if map_name and map_name != 'Stop Bot':
        image_name = f"{map_name}{extension}"
        sky_pixel_coordinates = locateOnScreen(all_images[image_name], region=sky_region_below, confidence=0.7)
        if sky_pixel_coordinates:
            x, y, x_thick, y_thick = sky_pixel_coordinates
            dist_calculator(y)
        else:
            sky_pixel_coordinates = locateOnScreen(all_images[image_name], region=sky_region_above, confidence=0.7)
            if sky_pixel_coordinates:
                x, y, x_thick, y_thick = sky_pixel_coordinates
                dist_calculator(y)
            else:
                dist_calculator('-')


def map_selector():
    global map_name
    maps = {'1': 'Ascent', '2': 'Bind', '3': 'Breeze', '4': 'Haven', '5': 'Icebox', '6': 'Split', '7': 'Stop Bot'}
    while True:
        system_caller('cls')
        print(f'Currently:  {map_name}')
        for _ in maps:
            print(_, maps[_])
        map_name = maps[input()]


def main_thread():
    while True:
        sleep(1)
        while True:
            if map_name and map_name != 'Stop Bot':
                pixel_finder()
                sleep(1 / fps)


molly = {(0, 13): 68,
(14, 16): 67,
(70, 83): 63,
(84, 96): 62,
(97, 102): 61,
(116, 119): 60,
(137, 142): 58,
(143, 153): 57,
(154, 163): 56,
(164, 172): 55,
(173, 184): 54,
(185, 193): 53,
(194, 203): 52,
(204, 211): 51,
(212, 219): 50,
(220, 229): 49,
(230, 238): 48,
(239, 247): 47,
(248, 254): 46,
(255, 262): 45,
(263, 269): 44,
(270, 277): 43,
(278, 285): 42,
(286, 293): 41,
(294, 299): 40,
(300, 305): 39,
(306, 312): 38,
(313, 318): 37,
(319, 324): 36,
(325, 333): 35,
(334, 340): 34,
(341, 345): 33,
(346, 353): 32,
(354, 360): 31,
(361, 365): 30,
(366, 373): 29,
(374, 376): 28,
(377, 382): 27,
(383, 390): 26,
(391, 397): 25,
(398, 402): 24,
(403, 408): 23,
(409, 414): 22,
(415, 421): 21,
(422, 427): 20,
(428, 434): 19,
(435, 439): 18,
(440, 446): 17,
(447, 449): 16,
(450, 455): 15}
smoke = {(0, 5): 40,
(6, 17): 39,
(70, 81): 37,
(82, 103): 36,
(116, 120): 35,
(138, 142): 34,
(143, 160): 33,
(161, 178): 32,
(179, 194): 31,
(195, 210): 30,
(211, 224): 29,
(225, 238): 28,
(239, 253): 27,
(254, 266): 26,
(267, 279): 25,
(280, 293): 24,
(294, 306): 23,
(307, 317): 22,
(318, 328): 21,
(329, 340): 20,
(341, 351): 19,
(352, 363): 18,
(364, 373): 17,
(374, 384): 16,
(385, 394): 15,
(395, 404): 14,
(405, 415): 13,
(416, 425): 12,
(426, 436): 11,
(437, 446): 10,
(447, 458): 9}

smoke_1080p = {}
for _range in smoke:
    for _ in range(_range[0], _range[1]+1):
        smoke_1080p[_] = smoke[_range]
molly_1080p = {}
for _range in molly:
    for _ in range(_range[0], _range[1]+1):
        molly_1080p[_] = molly[_range]

for _map in maps.values():
    image_name = f"{_map}{extension}"
    with open(gettempdir()+'\\'+image_name, 'wb') as img_file:
        img_file.write(get(f"https://raw.githubusercontent.com/BhaskarPanja93/ValorantViperUtility/master/1080p%20sky/{_map}.PNG").content)
        img_file.close()
    all_images[image_name] = Image.open(gettempdir()+'\\'+image_name)

Thread(target=create_smoke_overlay).start()
sleep(0.1)
Thread(target=create_molly_overlay).start()
sleep(0.1)
Thread(target=map_selector).start()
sleep(0.1)
Thread(target=main_thread).start()
