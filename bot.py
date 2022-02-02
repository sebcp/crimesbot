from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

img = Image.open("img-base.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("jarmstrongbold.ttf", 16)
msg = "covid-19"
w,h = font.getsize(msg)
x1 = 465
y1 = 180
x2 = 570
y2 = 215
x = (x1 + x2)/2-w
y = (y1 + y2)/2-h
draw.rectangle([x1, y1, x2, y2],outline ="red")
draw.text(((x),(y)), msg, font=font, fill="black")
img.save('sample-out.png')