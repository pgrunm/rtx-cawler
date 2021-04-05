import logging
import os
import re
from datetime import datetime

import requests
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater


def check_cards():

    urls = [
        'https://www.alternate.de/ZOTAC/GeForce-RTX-3060-TWIN-EDGE-OC-Grafikkarte/html/product/1715299',
        'https://www.alternate.de/GIGABYTE/GeForce-RTX-3060-EAGLE-OC-12G-Grafikkarte/html/product/1723539'
    ]
    reply_msg = ''
    for url in urls:
        # Get the content of the URL
        logging.info(f'Rufe {url} auf...')
        try:
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
            response = requests.get(url)

            # Check the response for it's content
            if response.status_code == 200:
                logging.debug(f'Statuscode of url {url} is 200')
                # Check for the hit
                if response.text.find('Auf Lager') != -1:
                    logging.info(f'Hit! Ist auf Lager bei {url}')
                    reply_msg += f'Grafikkarte verfügbar unter: {url}\n'

                # No hit found
                elif response.text.find('Artikel kann derzeit nicht gekauft werden') != -1:
                    logging.info('Kein Hit! Nicht verfügbar!')
                # Something went wrong?!
                else:
                    logging.error(f'Content nicht erkannt! URL: {url}')
            else:
                logging.warning(
                    f'Statuscode of url {url} is {response.status_code}')
        except Exception as e:
            logging.error(f'Error while getting url: {url}')
            logging.error(f'Error: {e}')

    if reply_msg == '':
        logging.info('Keine Hits. Sende keine Message...')
    else:
        logging.debug(f'Content reply_msg: {reply_msg}')
        return reply_msg


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f'Hello Master {update.effective_user.first_name}')


def status(update: Update, context: CallbackContext) -> None:
    logging.info('Status command was called!')
    reply_text = check_cards()
    if reply_text != None:
        logging.debug(
            f'Reply_text is not empty, replying message to chat -319659297 with content: {reply_text}')

        # Reply with url where the card is available
        update.message.reply_text(
            f'{reply_text}')
    else:
        # No hits available :()
        update.message.reply_text(
            f'Aktuell leider keine Hits! :(')


def callback_minute(context: CallbackContext):
    reply_text = check_cards()
    if reply_text != None:
        logging.debug(
            f'Reply_text is not empty, replying message to chat -319659297 with content: {reply_text}')
        context.bot.send_message(chat_id='-319659297',
                                 text=reply_text)
    else:
        pass


if __name__ == "__main__":
    log_level = ''
    # Read the logging configuration from environment variable
    log_level = os.getenv('log_level', default='INFO').upper()

    # Logging configuration
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=log_level, filename='bot.log', encoding='utf-8', filemode='w')
    logging.info(f'Bot started with log level {logging.root.level}!')
    try:
        logging.debug('Reading API key...')
        # updater = Updater(
        # '', use_context=True)
        updater = Updater(os.environ['bot_api_key'], use_context=True)
    except Exception as e:
        print(f'Erro: {e}')
        logging.debug(f'Failed to read API key with error: {e}')

    # Add Commands
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('status', status))

    # Schedule the crawling
    j = updater.job_queue
    job_minute = j.run_repeating(callback_minute, interval=60*30, first=10)

    updater.start_polling()
    updater.idle()
