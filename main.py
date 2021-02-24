
from windows import is_admin
from nebula import runNebula
import threading
import os
from storage import Storage
import pystray
from PIL import Image, ImageDraw
from pystray import Menu, MenuItem
from plyer import filechooser
import pathlib
import sys

if getattr(sys, 'frozen', False):
    directory = os.path.dirname(sys.executable)
elif __file__:
    directory = os.path.dirname(__file__)

store = Storage()
thread = None
threadDone = True
logStr = ''

def create_image(color=250):
    # Generate an image and draw a pattern
    width=16
    height=16
    color1=20
    color2=color
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def setup(icon):
    icon.visible = True
def log(line):
    file1 = open(str(directory)+os.sep+'thread.log', 'a+')
    file1.write(line) 
    file1.close() 
def tDone():
    global threadDone
    threadDone=True
    icon.icon = create_image()
def connect(icon, item):
    global thread, threadDone
    if threadDone:
        thread = threading.Thread(target=runNebula, args=("nebula", log, store.get('executable_path'), store.get('config_path'), directory, tDone))
        thread.daemon = True
        thread.start()
        icon.icon = create_image((51,255,51))
        threadDone=False
def config(icon, item):
    paths = filechooser.open_file(title="Choose Nebula Config")    
    if len(paths) > 0:
        store.add('config_path', paths[0])
def quit(icon, item):
    icon.stop()
def menu():
    return Menu(
    MenuItem(
        'Connect',
        connect),
    MenuItem(
        'Config',
        config),
    MenuItem(
        'Quit',
        quit)
        )

if __name__ == '__main__':
    log(str(directory)+"\n")
    icon = pystray.Icon('test name', create_image(), menu=menu())
    #create_image().show()
    icon.run(setup)