from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

MAX_CHAR_16 = 6

def template(msg):
    img = Image.open("img-base.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("jarmstrongbold.ttf", 16)
    w,h = font.getsize(msg)
    x1 = 464
    y1 = 180
    x2 = 572
    y2 = 215
    x = (x1 + x2 - w)/2
    y = (y1 + y2 - h)/2
    #draw.rectangle([x1, y1, x2, y2],outline ="red")
    draw.text(((x),(y)), msg, font=font, fill="black")
    img.save('sample-out.png')