import imageio
import filetype
import numpy
from moviepy.editor import *
import time
import PIL
from PIL import Image

def rescale(factor, im):
    w, h = im.size
    w_, h_ = w // factor, h // factor
    temp_im = im.resize((w_, h_))
    out_im = temp_im.resize((w, h), Image.NEAREST)
    return out_im

filename = "car.mp4"
kind = filetype.guess(filename)
if kind is None or kind.extension not in ["jpg", "mp4", "gif", "png"]:
    print("Filetype not supported! Ping luke if you think this should be a valid filetype")
    print(kind)
    exit()

ext = kind.extension
ext_dict = {
    "png" : "PNG-PIL",
    "jpg" : "JPEG-PIL",
    "gif" : "GIF-PIL",
    "mp4" : "FFMPEG"
}

reader = imageio.get_reader(filename, format=ext_dict[ext])
print(reader.format)
print(reader.get_meta_data())
fps = reader.get_meta_data()['fps']
out_file = "out.mp4" if ext == "mp4" else "out.gif"
#do thing to slim gif
writer = imageio.get_writer(out_file,fps=fps)
for im in reader:
    new_im = Image.fromarray(im)
    fmt_img = rescale(10, new_im)
    writer.append_data(numpy.array(fmt_img))
#    writer.append_data(im)
writer.close()
t0 = time.time()

audio_clip = AudioFileClip(filename)
video_clip = VideoFileClip(out_file)
video_clip2 = video_clip.set_audio(audio_clip)
video_clip2.write_videofile("1" + out_file)