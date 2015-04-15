import subprocess

p1 = subprocess.Popen(['python', 'server.py'])
p2 = subprocess.Popen(['python', 'run.py'])

import webbrowser
import os
new = 2
url = os.path.join(os.getcwd(),'index.html')
webbrowser.open(url,new=new)


def goodbye():
    p1.kill()
    p2.kill()

import atexit
atexit.register(goodbye)

while True:
    pass

