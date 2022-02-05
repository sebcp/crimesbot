import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ParseMode

from image import generate_image, get_image_bio
from auth import *

logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def send_error_message(update, context):
    message = "El texto es muy largo. El bot soporta hasta 27 caracteres."
    logging.error(f'User {update.message.chat_id} - Error: Texto muy largo')
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=message, parse_mode=ParseMode.MARKDOWN)


def send_help(update, context):
    message = "El bot puede recibir hasta 27 caracteres para rellenar el template del panel de Pop Team Epic."
    logging.info(f'User {update.message.chat_id} - Llamó a /help')
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
    logging.info(
        f'User {update.message.chat_id} - Llamó a /crimes con el mensaje "{message}"')
    context.bot.sendPhoto(chat_id=update.message.chat_id, photo=bio)


if __name__ == '__main__':
    updater = Updater(
        token=token, use_context=True)
    dispatcher = updater.dispatcher
    help_handler = CommandHandler('help', send_help)
    crimes_handler = CommandHandler('crimes', send_crimes)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(crimes_handler)
    updater.start_polling()
