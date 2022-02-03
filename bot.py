from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap

MAX_CHAR_16 = 6
MAX_CHAR_12 = 15
MAX_CHAR_10 = 27

def template(msg):
    img = Image.open("img-base.png")
    draw = ImageDraw.Draw(img)
    x1 = 464
    x2 = 572
    width = len(msg)
    print(width)
    if width<=MAX_CHAR_16:
        font = ImageFont.truetype("jarmstrongbold.ttf", 16)
        w,h = font.getsize(msg)
        y1 = 180
        y2 = 215
        x = (x1 + x2 - w)/2
        y = (y1 + y2 - h)/2
        #draw.rectangle([x1, y1, x2, y2],outline ="red")
        draw.text(((x),(y)), msg, font=font, fill="black")
    elif width > MAX_CHAR_16 and width <= MAX_CHAR_12:
        font = ImageFont.truetype("jarmstrongbold.ttf", 12)
        msg_wrapped = textwrap.wrap(msg,width=8)
        pad = 2
        w, h = draw.textsize(msg_wrapped[0], font=font)
        y1 = 164
        y2 = 199
        current_h = (y1 + y2 - h)/2
        for line in msg_wrapped:
            w, h = draw.textsize(line, font=font)
            x = (x1 + x2 - w)/2
            draw.text((x, current_h), line, font=font, fill="black")
            current_h += h + pad
    elif width > MAX_CHAR_12:
        font = ImageFont.truetype("jarmstrongbold.ttf", 10)
        msg_wrapped = textwrap.wrap(msg,width=9)
        pad = 2
        w, h = draw.textsize(msg_wrapped[0], font=font)
        y1 = 168
        y2 = 203
        current_h = (y1 + y2 - h)/2
        for line in msg_wrapped:
            w, h = draw.textsize(line, font=font)
            x = (x1 + x2 - w)/2
            draw.text((x, current_h), line, font=font, fill="black")
            current_h += h + pad
    img.save('sample-out.png')

template("no se que hacer")