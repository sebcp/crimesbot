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
    global draw
    global x
    global current_h
    global pad

    img = Image.open("img-base.png")
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
    return img.convert('RGB')

def get_image_bio(img):
    bio = BytesIO()
    bio.name = 'image.jpeg'
    img.save(bio, 'JPEG', quality=100)
    bio.seek(0)
    return bio

def send_error_message(update, context):
    message = "El texto es muy largo. El bot soporta hasta 27 caracteres."
    context.bot.sendMessage(chat_id=update.message.chat_id,
                           text=message, parse_mode=ParseMode.MARKDOWN)

def send_help(update, context):
    message = "El bot puede recibir hasta 27 caracteres para rellenar el template del panel de Pop Team Epic."
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=message, parse_mode=ParseMode.MARKDOWN)

def send_crimes(update, context):
    args = context.args
    if (len(context.args)) < 1:
        return
    message = ' '.join(args)
    if len(message) > 27:
        return send_error_message(update, context)
    img = generate_image(message)
    bio = get_image_bio(img)
    context.bot.sendPhoto(chat_id=update.message.chat_id, photo=bio)

if __name__ == '__main__':
    updater = Updater(token='token', use_context=True)
    dispatcher = updater.dispatcher
    help_handler = CommandHandler('help', send_help)
    crimes_handler = CommandHandler('crimes', send_crimes)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(crimes_handler)
    updater.start_polling()