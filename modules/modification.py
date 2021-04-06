from PIL import Image
import asyncio
import tempfile
import requests
import time
import os   
import filetype


class ImageScaler():
    def __init__(self, url):
        self.url = url

    def scale_image(self):
        (fd, filename) = tempfile.mkstemp()
        try:
            tfile = os.fdopen(fd, "wb")
            #fool discord into authorizing our request
            r = requests.get(self.url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'})
            tfile.write(r.content)
            tfile.close()
            print(filename)
            #look at image type with pillow
            print(filetype.guess(filename))
            img = Image.open(filename)
            print(img.format)
            img.close()
        except Exception as e:
            print("Could not download image")
            print(e)
        finally:
            os.remove(filename)
        



img = ImageScaler("https://cdn.discordapp.com/attachments/780833671509966848/827245139591823400/video0.mp4")
img.scale_image()
