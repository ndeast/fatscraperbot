import tokens as tok
import json
import os
import time
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


recs = []
last_five_recs = ""
latest_release = ""
new_recs = 0
poll = 10

def get_last_n_recs(n, recs):
    if n > 0:
        return recs[-n:]
    else:
        return []

def print_last_five(recs):
    l = len(recs) - 1 
    str = ""
    for i in range(l, (l - 5), -1):
        str += format_release(recs[i])
    return str

def parse_recs():
    temp_recs = []
    if os.path.exists(tok.JSONFILE):
        with open(tok.JSONFILE, 'r') as f:
            temp_recs = json.load(f)
    else:
        print("file not found")
    return temp_recs

def get_num_new_recs():
    new_releases = 0
    if os.path.exists(tok.NEWRELEASES):
        with open(tok.NEWRELEASES, 'r') as c:
            num = c.readline().rstrip()
            new_releases = int(num) if num.isdigit() else 0
    return new_releases

def handle_new_releases(recs, new_recs):
    tempstr = ""
    new_recs = get_last_n_recs(get_num_new_recs(), recs)
    for rec in new_recs:
        tempstr += format_release(rec)
    # os.remove(tok.NEWRELEASES)
    return tempstr

def format_release(rec):
    return (
        f"Title: {rec.get('title')}\n"
        f"Artist: {rec.get('artist')}\n"
        f"Release Date: {rec.get('release_date')}\n"
        f"Link: {rec.get('link')}\n\n"
    )

# Telegram command handlers
def start(update, context):
    """Send a message when command /start is issued."""
    update.message.reply_text("Working")

def last(update, context):
    update.message.reply_text(latest_release)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(tok.TELEGRAMBOT, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("last", last))

    dp.add_error_handler(error)

    updater.start_polling()

    tr = 0
    while 1:
        if tr == poll:
            tr = 0

            if (new_recs := get_num_new_recs()):
                logger.info("New Release!")
                recs = parse_recs()
                latest_release = handle_new_releases(recs, new_recs)
        
        time.sleep(10)
        tr += 10

    updater.idle()


recs = parse_recs()
last_five_recs = print_last_five(recs)
latest_release = format_release(recs[-1])

if __name__ == '__main__':
    main()