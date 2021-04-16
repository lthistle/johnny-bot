from PIL import Image
import asyncio
import filetype
import imageio
# from moviepy.editor import *
import tempfile
import requests
import time
import os   
import filetype
import numpy

ext_dict = {
    "png" : "PNG-PIL",
    "jpg" : "JPEG-PIL",
    "gif" : "GIF-PIL",
    "mp4" : "FFMPEG"
} #ext_dict.keys() represents supported extensions

class MediaScaler():
    """Set of classes used to rescale images, gifs, and videos (for ?alanify command)"""
    def __init__(self):
        self.local_files = [] #list of local files to be deleted later
    
    async def download(self, url):
        fd, filename = tempfile.mkstemp()
        try:
            tfile = os.fdopen(fd, "wb")
            #fool discord into authorizing our request
            r = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'})
            #write to tempfile
            tfile.write(r.content)
            tfile.close()
            #save as local_file
            self.local_files.append(filename)
            return (tfile, filename)
        except Exception as e:
            print("Could not download image")
            print(e)

    async def remove_all_local(self):
        for lf in self.local_files:
            try:
                os.remove(lf)
            except Exception as e:
                print("Could not delete local files!")
                print(e)

    async def rescale(self, factor, img : Image):
        w, h = img.size
        w_, h_ = w // factor, h // factor
        img_ = img.resize((w_, h_))
        img_out = img_.resize((w, h), Image.NEAREST)
        return img_out

    async def get_extension(self, filename):
        kind = filetype.guess(filename)
        print("HIHIIIII")
        print(filename)
        print(kind)
        print(kind)
        if kind is None or kind.extension not in ext_dict.keys():
            print("Filetype not supported! Ping luke if you think this is a mistake")
            print(kind)
        else:
            return kind.extension

    async def rewrite_media(self, scale_factor, filename):
        ext = await self.get_extension(filename)
        if ext is None: return
        reader = imageio.get_reader(filename, format=ext_dict[ext])
        out_filename = f"{filename}_out.{ext}"
        self.local_files.append(out_filename)
        #format imageio writer properly
        print(reader.get_meta_data())
        if ext == 'mp4':
            fps = reader.get_meta_data()['fps']
            writer = imageio.get_writer(out_filename, fps=fps)
        # elif ext == 'gif':
        #     duration = reader.get_meta_data()['duration']
        #     writer = imageio.get_writer(out_filename, mode='I', duration=5)
        #     print('pass')
        else:
            writer = imageio.get_writer(out_filename)
        #sequence each frame
        for im in reader:
            new_im = Image.fromarray(im)
            fmt_img = await self.rescale(scale_factor, new_im)
            writer.append_data(numpy.array(fmt_img))
        writer.close()
        #if file is mp4, re-add audio
        # if ext == 'mp4':
        #     audio_clip = AudioFileClip(filename)
        #     video_clip = VideoFileClip(out_filename)
        #     video_clip2 = video_clip.set_audio(audio_clip)
        #     video_clip2.write_videofile(out_filename)
        return (out_filename, ext)
#alanify:
#download file locally
#get filetype


# ms = MediaScaler()
# media_file, filename = ms.download("https://media.discordapp.net/attachments/775075293345742879/829045040126492722/album_1f0afvdo6.gif")
# print("downloaded", media_file, filename)

# rfname = ms.rewrite_media(10, filename)
# print(rfname)
# ms.remove_all_local()

