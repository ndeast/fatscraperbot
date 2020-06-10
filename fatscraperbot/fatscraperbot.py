import json
import os

def get_last_n_recs(n, recs):
    if n > 0:
        return recs[-n:]
    else:
        return []

def parse_recs(file):
    if os.path.exists(file):
        with open(file, 'r') as f, open('count', 'w') as c:
            recs = json.load(f)
            c.write(str(len(recs)))
    else:
        print("file not found")
    return recs

def updated_rec_count():
    count = 0
    if os.path.exists('count'):
        with open('count', 'r') as c:
            count = int(c.readline().strip())
    return count


rec_count = 32

recs = parse_recs('UpcomingRecords.json')

new_recs = (updated_rec_count() - rec_count)
print(get_last_n_recs(new_recs, recs))