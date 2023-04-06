import clipboard_monitor 
from PIL import Image, ImageGrab

def print_text(text):
	print("got text")
	print(text)

def print_files(files):
	print("got files")
	print(files)

def print_image():
	print("got image")
	image = ImageGrab.grabclipboard()
	image.save("./test.png")

clipboard_monitor.on_update(print)
clipboard_monitor.on_text(print_text)
clipboard_monitor.on_files(print_files)
clipboard_monitor.on_image(print_image)

clipboard_monitor.wait()
