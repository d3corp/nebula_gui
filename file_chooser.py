from tkinter.filedialog import askopenfilename
from tkinter import Tk     # from tkinter import Tk for Python 3.x



def chooseConfig():
    
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
   
