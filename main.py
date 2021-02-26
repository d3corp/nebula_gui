
from windows import is_admin
from nebula import Nebula
import threading
import os
from storage import Storage
import pystray
from PIL import Image, ImageDraw, ImageFont
from pystray import Menu, MenuItem
import pathlib
import sys
from tkinter.filedialog import askopenfilename
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from file_chooser import chooseConfig


if getattr(sys, 'frozen', False):
    directory = os.path.dirname(sys.executable)
elif __file__:
    directory = os.path.dirname(os.path.abspath(__file__))

store = Storage()
thread = None
threadDone = True
logStr = ''

def create_image(type="off"):
    # Generate an image and draw a pattern
    image = Image.open(directory+os.sep+"resources"+os.sep+"icon-"+type+".png")

    return image

def setup(icon):

    icon.visible = True
def log(line):
    file1 = open(str(directory)+os.sep+'nebula_gui.log', 'a+')
    file1.write(line) 
    file1.close() 
    
def tDone():
    global threadDone
    threadDone=True
    icon.icon = create_image()
def connect(icon, item):
    global thread, threadDone
    if threadDone:
        thread = Nebula(log, tDone, directory, store.get('config_path'))
        thread.daemon = True
        thread.start()
        icon.icon = create_image("connected")
        threadDone=False
def config(icon, item):
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    store.add('config_path', filename)
def quit(icon, item):
    global thread
    if thread is not None:
        log("disconnect")
        thread.disconnect()
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
    Tk().withdraw()
    icon = pystray.Icon('test name', create_image(), menu=menu())
    #create_image().show()
    icon.run(setup)