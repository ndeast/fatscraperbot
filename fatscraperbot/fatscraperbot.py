import tokens as tok
from FatScraper import FSData
import json
import os
import time
import logging
from uuid import uuid4
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

new_recs = 0
poll = 10

fs = FSData(tok.JSONFILE, tok.NEWRELEASES)

# Telegram command handlers
def start(update, context):
    """Send a message when command /start is issued."""
    update.message.reply_text("Working")

def last(update, context):
    update.message.reply_text(fs.latest_release)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(tok.TELEGRAMBOT, use_context=True)

    dp = updater.dispatcher
    bot = updater.bot

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("last", last))

    dp.add_error_handler(error)

    updater.start_polling()

    tr = 0
    while 1:
        if tr == poll:
            tr = 0

            if (fs.new_record_released()):
                logger.info("New Release!")
                fs.update()
                bot.send_message(tok.ADMINCHATID[0], fs.latest_release)
        
        time.sleep(10)
        tr += 10

    updater.idle()

if __name__ == '__main__':
    main()