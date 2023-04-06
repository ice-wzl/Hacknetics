#!/usr/bin/python3
import pyperclip
from termcolor import cprint 

while True:
    buffer_wait = pyperclip.waitForNewPaste()
    cprint("------------------------------------------------------------------", "red")
    print(buffer_wait.strip())
