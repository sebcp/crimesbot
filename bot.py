from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from io import BytesIO

import textwrap

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ParseMode

MAX_CHAR_16 = 7
MAX_CHAR_12 = 20
MAX_CHAR_10 = 27

def draw_multiple_lines(msg, font, x1, x2, current_h):
    for line in msg:
        w, h = draw.textsize(line, font=font)
        x = (x1 + x2 - w)/2
        draw.text((x, current_h), line, font=font, fill="black")
        current_h += h + pad

def generate_image(msg):
    img = Image.open("img-base.png")
    global draw
    global x
    global current_h
    global pad
    draw = ImageDraw.Draw(img)
    x1 = 464
    x2 = 572
    pad = 2
    width = len(msg)
    if width<=MAX_CHAR_16:
        font = ImageFont.truetype("jarmstrongbold.ttf", 16)
        w,h = font.getsize(msg)
        x = (x1 + x2 - w)/2
        y1 = 180
        y2 = 215
        y = (y1 + y2 - h)/2
        draw.text(((x),(y)), msg, font=font, fill="black")
    elif width > MAX_CHAR_16 and width <= MAX_CHAR_12:
        font = ImageFont.truetype("jarmstrongbold.ttf", 12)
        msg_wrapped = textwrap.wrap(msg,width=8)
        w, h = draw.textsize(msg_wrapped[0], font=font)
        if len(msg_wrapped) == 1:
            y1 = 180
            y2 = 215
        elif len(msg_wrapped) == 2:
            y1 = 172
            y2 = 207
        elif len(msg_wrapped) == 3:
            y1 = 164
            y2 = 199
        current_h = (y1 + y2 - h)/2
        draw_multiple_lines(msg_wrapped, font, x1, x2, current_h)
    elif width > MAX_CHAR_12:
        font = ImageFont.truetype("jarmstrongbold.ttf", 10)
        msg_wrapped = textwrap.wrap(msg,width=9)
        w, h = draw.textsize(msg_wrapped[0], font=font)
        y1 = 166
        y2 = 201
        current_h = (y1 + y2 - h)/2
        draw_multiple_lines(msg_wrapped, font, x1, x2, current_h)
    #img.save('sample-out.png')
    return img

def get_image_bio(img):
    bio = BytesIO()
    bio.name = 'image.jpeg'
    img.save(bio, 'JPEG', quality=100)
    bio.seek(0)
    return bio