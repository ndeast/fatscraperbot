import tokens as tok
import json
import os

recs = []

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
            new_releases = int(c.read())
    return new_releases

def handle_new_releases(recs):
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
handle_new_releases(recs)