
import pip
from importlib import import_module
requirements = ['pyautogui', 'tkinter']
for i in requirements:
    try:
        globals()[i] = import_module(i)
        del globals()[i]
    except ModuleNotFoundError:
        pip.main(['install', i])
        globals()[i] = import_module(i)
del import_module
pip.main(['install', 'opencv_python'])
pip.main(['install', 'pillow'])
del pip


from tkinter import Tk, Label
from time import sleep
from threading import Thread
from pyautogui import locateOnScreen, size
from os import getcwd
from subprocess import call



fps = 10
map_name = ''
molly = None
smoke = None
screen_res = size()

sky_region_above = (int(0.491 * screen_res[0]), 0, int(0.0162 * screen_res[0]), int(0.03 * screen_res[1]))
sky_region_below = (int(0.491 * screen_res[0]), int(0.056 * screen_res[1]), int(0.016 * screen_res[0]), int(0.38333 * screen_res[1]))

dist_molly = '-'
dist_smoke = '-'

molly_1080p = eval(open(getcwd()+'/molly1080.txt','r').read())
smoke_1080p = eval(open(getcwd()+'/smoke1080.txt','r').read())


def molly_overlay():
    global molly
    molly_label = Tk()
    molly = Label(molly_label, text='-', font=('Libre Bodoni', '10'), fg='black', bg='red')
    molly.master.overrideredirect(True)
    molly.master.geometry("+400-0")
    molly.master.wm_attributes("-topmost", True)
    molly.master.wm_attributes("-disabled", True)
    molly.master.wm_attributes("-transparentcolor", "white")
    molly.pack()
    molly_label.mainloop()


def smoke_overlay():
    global smoke
    smoke_label = Tk()
    smoke = Label(smoke_label, text='-', font=('Libre Bodoni', '10'), fg='black', bg='red')
    smoke.master.overrideredirect(True)
    smoke.master.geometry("-400-0")
    smoke.master.wm_attributes("-topmost", True)
    smoke.master.wm_attributes("-disabled", True)
    smoke.master.wm_attributes("-transparentcolor", "white")
    smoke.pack()
    smoke_label.mainloop()


def update_displayed_values(molly_dist, smoke_dist):
    global molly, smoke
    molly.config(text=molly_dist)
    smoke.config(text=smoke_dist)


def dist_calculator(bar):
    smoke_dist = '-'
    molly_dist = '-'
    if bar == '-':
        smoke_dist = molly_dist = bar
    else:
        x, y, x_thick, y_thick = bar
        bar = int((int(y) * 1080) / screen_res[1])
        for x in molly_1080p:
            if bar < x[0]:
                molly_dist = molly_1080p[x]
                break
        for x in smoke_1080p:
            if bar < x[1]:
                smoke_dist = smoke_1080p[x]
                break
    update_displayed_values(molly_dist, smoke_dist)


def pixel_finder():
    global map_name
    sky_pixel_location = getcwd() + '/' + str(screen_res[1]) + 'p sky' + '/'
    extension = '.png'
    sky_pixel_coordinates = locateOnScreen(sky_pixel_location + map_name + extension,region=sky_region_below, confidence=0.7)
    if sky_pixel_coordinates:
        dist_calculator(sky_pixel_coordinates)
    else:
        sky_pixel_coordinates = locateOnScreen(sky_pixel_location + map_name + extension,region=sky_region_above, confidence=0.7)
        if sky_pixel_coordinates:
            dist_calculator(sky_pixel_coordinates)
        else:
            dist_calculator('-')



def map_selector():
    global map_name
    call('cls', shell=True)
    maps = {'1': 'Ascent', '2': 'Bind', '3': 'Breeze', '4': 'Haven', '5': 'Icebox', '6': 'Split', '7': 'Stop Bot'}
    while True:
        for _ in maps:
            print(_, maps[_])
        map_name = maps[input()]
        print(f'selected  {map_name}')


Thread(target=smoke_overlay).start()
Thread(target=molly_overlay).start()
Thread(target=map_selector).start()


while True:
    while True:
        if map_name:
            if map_name != 'Stop Bot':
                Thread(target=pixel_finder).start()
                sleep(1 / fps)
    sleep(1)
