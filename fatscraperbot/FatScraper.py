import os
import json
class FSData:

    def __init__(self, datafile, countfile):
        self.datafile = datafile
        self.countfile = countfile
        self.recs = self.__parse_recs()
        self.last_five_recs = self.__print_last_five()
        self.latest_release = self.format_release(self.recs[-1])
        self.new_recs = 0

    def __get_last_n_recs(self, n, recs):
        if n > 0:
            return self.recs[-n:]
        else:
            return []

    def __print_last_five(self):
        last_five = self.__get_last_n_recs(5, self.recs)
        str = ""
        for rec in last_five:
            str += self.format_release(rec)
        return str

    def __parse_recs(self):
        temp_recs = []
        if os.path.exists(self.datafile):
            with open(self.datafile, 'r') as f:
                temp_recs = json.load(f)
        else:
            print("file not found")
        return temp_recs

    def __get_num_new_recs(self):
        new_releases = 0
        if os.path.exists(self.countfile):
            with open(self.countfile, 'r') as c:
                num = c.readline().rstrip()
                new_releases = int(num) if num.isdigit() else 0
        return new_releases

    def __handle_new_releases(self):
        tempstr = ""
        self.recs = self.__parse_recs()
        new_recs = self.__get_last_n_recs(self.__get_num_new_recs(), self.recs)
        for rec in new_recs:
            tempstr += self.format_release(rec)
        os.remove(self.countfile)
        self.latest_release = tempstr

    def format_release(self, rec):
        return (
            f"Title: {rec.get('title')}\n"
            f"Artist: {rec.get('artist')}\n"
            f"Release Date: {rec.get('release_date')}\n"
            f"Link: {rec.get('link')}\n\n"
        )

    def update(self):
        self.__handle_new_releases()

    def new_record_released(self):
        return self.__get_num_new_recs()