import urllib, urllib.request
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import os
import subprocess
import random

Tk().withdraw()
download_path = "https://raw.githubusercontent.com/paulnbrd/PyFrame/master/src/pyframe.py"
requirements_path = "https://raw.githubusercontent.com/paulnbrd/PyFrame/master/src/requirements.txt"

def update_pyframe(directory) :
    with urllib.request.urlopen(requirements_path) as response:
        res = response.read()
        random_int = str(random.randint(2000000000,2147483647))+str(random.randint(2000000000,2147483647))
        open(directory+"/"+random_int+".txt",mode="w").write(res.decode("utf-8"))
        print("Installing dependancies...")
        subprocess.call('pip install -r '+directory+'/'+random_int+'.txt', shell=True)
        os.remove(directory+"/"+random_int+".txt")
    with urllib.request.urlopen(download_path) as response :
       res = response.read()
       open(directory+"/pyframe.py",mode="w",encoding="utf-8").write(res.decode("utf-8"))
directory =  askdirectory(title='Open the directory where the pyframe.py should be saved.')
if os.path.isfile(directory+"/pyframe.py") :
    if askyesno("Attention !","Le fichier pyframe.py existe déjà ! Tout son contenu sera écrasé si vous continuez") :
        update_pyframe(directory)
else :
    update_pyframe(directory)