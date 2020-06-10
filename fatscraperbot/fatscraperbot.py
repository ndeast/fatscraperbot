import tokens as tok
import json
import os

rec_count = 0
recs = []

def get_last_n_recs(n, recs):
    if n > 0:
        return recs[-n:]
    else:
        return []

def parse_recs():
    if os.path.exists(tok.JSONFILE):
        with open(tok.JSONFILE, 'r') as f, open(tok.COUNT, 'w') as c:
            recs = json.load(f)
            c.write(str(len(recs)))
    else:
        print("file not found")
    return recs

def updated_rec_count():
    count = 0
    if os.path.exists(tok.COUNT):
        with open(tok.COUNT, 'r') as c:
            count = int(c.readline().strip())
    return count

def new_release(recs, rec_count):
    recs = parse_recs()
    new_rec_count = updated_rec_count()
    num_new_recs = (new_rec_count - rec_count)
    rec_count = new_rec_count
    print(get_last_n_recs(num_new_recs, recs))

rec_count = updated_rec_count() - 1
new_release(recs, rec_count)
# recs = parse_recs()
# if rec_count != len(recs):
#     print(get_last_n_recs((len(recs) - rec_count), recs))