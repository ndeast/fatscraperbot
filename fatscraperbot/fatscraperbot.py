import tokens as tok
import json
import os
import time
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

recs = []
new_recs = 0
poll = 300

def get_last_n_recs(n, recs):
    if n > 0:
        return recs[-n:]
    else:
        return []

def parse_recs():
    if os.path.exists(tok.JSONFILE):
        with open(tok.JSONFILE, 'r') as f:
            recs = json.load(f)
    else:
        print("file not found")
    return recs

def get_num_new_recs():
    new_releases = 0
    if os.path.exists(tok.NEWRELEASES):
        with open(tok.NEWRELEASES, 'r') as c:
            num = c.readline().rstrip()
            new_releases = int(num) if num.isdigit() else 0
            print(new_releases)
    return new_releases

def handle_new_releases(recs, new_recs):
    new_recs = get_last_n_recs(get_num_new_recs(), recs)
    for rec in new_recs:
        print(format_release(rec))

def format_release(rec):
    return (
        f"Title: {rec.get('title')}\n"
        f"Artist: {rec.get('artist')}\n"
        f"Release Date: {rec.get('release_date')}\n"
        f"Link: {rec.get('link')}\n"
    )

recs = parse_recs()
tr = 0
while 1:
    if tr == poll:
        tr = 0

        if (new_recs := get_num_new_recs()):
            handle_new_releases(recs, new_recs)
            os.remove(tok.NEWRELEASES)
    
    time.sleep(10)
    tr += 10