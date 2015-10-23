import os
import ctypes
import subprocess
import textwrap
import pyHook
import pythoncom
from pyHook import HookManager
from pyHook.HookManager import HookConstants
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import thread
import getpass



def update_desk():
    user = "public"
    filepath="c:\\Users\\"+user+"\\harsh.md"
    app = r'c:\Windows\Notepad.exe'
    
    pid = subprocess.Popen([app, filepath])
    pid.wait()
    fontname = "arial.ttf"
    with open(filepath, "r") as myfile:
        data = myfile.read()
    linedata = data.split("\n")
    if len(linedata) > 20:
        fontsize = 10
    else:
        fontsize = 20
    y_text = 120
    w = 768
    imgpath="c:\\Users\\"+user+"\\harsh"
    font = ImageFont.truetype(fontname, fontsize)
    img = Image.new('RGB', (1024, 768), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for datal in linedata:
        lines = textwrap.wrap(datal, width=60)

        for line in lines:
            width, height = font.getsize(line)
            d.text(((w - width)/2+150, y_text), line, font=font, fill=(0, 0, 0))
            print(line)
            y_text += height+5

    img.save(imgpath, 'png')
    path = os.path.abspath(imgpath)
    ctypes.windll.user32.SystemParametersInfoA(20, 0, path, 1 | 2)
    


def OnKeyboardEvent2(event):
    if HookConstants.VKeyToID('VK_ESCAPE') == event.KeyID:
        hooks_manager.KeyDown = OnKeyboardEvent1


def OnKeyboardEvent1(event):
    if event.Key == "Oem_3":
        thread.start_new_thread(update_desk,())
        
        hooks_manager.KeyDown = OnKeyboardEvent2

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent2
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
