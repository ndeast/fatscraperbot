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

def get_new_rec_ids():
    new_releases = []
    if os.path.exists(tok.NEWRELEASES):
        with open(tok.NEWRELEASES, 'r') as c:
            new_releases = [int(l.rstrip("\n")) for l in c]
    return new_releases

def handle_new_releases(recs):
    new_rec_ids = get_new_rec_ids()
    for rec_id in new_rec_ids:
        print(format_release(recs[rec_id]))

def format_release(rec):
    return (
        f"Title: {rec.get('title')}\n"
        f"Artist: {rec.get('artist')}\n"
        f"Release Date: {rec.get('release_date')}\n"
        f"Link: {rec.get('link')}\n"
    )

recs = parse_recs()
handle_new_releases(recs)