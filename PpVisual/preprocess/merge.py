
import re
import string
import json
import math
import pandas as pd
from nltk.tokenize import word_tokenize
urlReg = r"^(?:([A-Za-z]+):)?(\/{0,3})([0-9.\-A-Za-z]+)(?::(\d+))?(?:\/([^?#]*))?(?:\?([^#]*))?(?:#(.*))?$"
entityRe = r'\[\@.*?\#.*?\*\](?!\#)'


def get_word_count(text, returnsequences=False, retuenlist = False):
    tokens = word_tokenize(text)
    words = [word for word in tokens if re.search(r"[\w]", word)]
    if returnsequences:
        return " ".join(words)
    elif retuenlist:
        return words
    else:
        return len(words)


def getLabelPair(text, pattern=entityRe):
    label_pair = re.search(pattern, text)
    if label_pair:
        new_string_list = label_pair.group().strip('[@*]').rsplit('#', 1)
        par_text = new_string_list[0]
        label = new_string_list[1]
        label = "Legal Basis" if label.lower() == "legal basis" else label
        label = "User Control" if label == "User Choice/Control" else label
        sentiment = 0
    else:
        par_text = text
        label = "Other"
        sentiment = 0
    return {"text": par_text, "label": label, "sentiment": sentiment}


def removeLabel(text):
    return text.replace("[@", "").rsplit('#', 1)[0]


class MergeFollows:
    def __init__(self, document, isBMES = False):
        self.text = document
        self.isBMES = isBMES
        self._start = "start"
        self._unTAG = "unTAG"
        self._item = "item"
        self._ultag = r"\[@Start#\]"
        self.par_list = self.text.split('\n')
        if isBMES:
            self.par_dict = [{"par": getLabelPair(par)["text"],
                              "tag": self._unTAG,
                              "label": getLabelPair(par)["label"]}
                             for par in self.par_list]

        else:
            self.par_dict = [{"par": par, "tag": self._unTAG} for par in self.par_list]
        self._merged_par = []
        self.theEndofStr = ("or", "and", ";", ",")
        self._initDict()

    def _initDict(self):
        for key, item in enumerate(self.par_dict):
            text = item["par"].strip()
            last = self._getLastItem(key)
            next = self._getNextItem(key)

            maybe = key != 0 and (self.par_dict[key - 1]["tag"] == self._start or self.par_dict[key - 1]["tag"] == "null")\
                    and len (self.par_dict[key]["par"].strip ()) == 0

            #  as follows: check if have :
            if self._isStart(key):
                self.par_dict[key]["tag"] = self._start

            elif maybe:
                self.par_dict[key]["tag"] = "null"

            # after :, the first str must be the item
            elif key != 0 and self.par_dict[key-1]["tag"] == self._start or self.par_dict[key-1]["tag"] == "null":
                self.par_dict[key]["tag"] = self._item

            # if the fist char is special char: have problem with two merged list.
            elif self._maybeItem(key) and not text[0].isalnum():
                self.par_dict[key]["tag"] = self._item
            elif self._maybeItem(key, notNULL=False) and not last[0].isalnum() and last[0] == next[0]:
                self.par_dict[key]["tag"] = self._item
            # such as "to access  your personal information."
            elif self._maybeItem(key) and text[:3].lower() == "to ":
                self.par_dict[key]["tag"] = self._item
            elif self._maybeItem(key, notNULL=False) and last[:3].lower() == "to " and last[:3] == next[:3]:
                self.par_dict[key]["tag"] = self._item
            elif self._maybeItem(key) and text[:8].lower() == "request ":
                self.par_dict[key]["tag"] = self._item
            elif self._maybeItem(key, notNULL=False) and last[:8].lower() == "request " and last[:8] == next[:8]:
                self.par_dict[key]["tag"] = self._item
            # elif self._maybeItem(key, notNULL=False) and (text.split(' ')[0].strip().isdigit() or
            #                                               text.split('.')[0].strip().isdigit()):
            #     self.par_dict[key]["tag"] = self._item
            # such as "Request a structured electronic version of your information;"
            # or "Request a structured electronic version of your information; and"
            # Besides set the next str to the item
            elif self._maybeItem(key) and text.endswith(self.theEndofStr):
                self.par_dict[key]["tag"] = self._item
                if key + 1 != len(self.par_dict):
                    self.par_dict[key + 1]["tag"] = self._item
            # the last item is start with number end this item is also start with item
            elif self._maybeItem(key) and text.strip()[0].isdigit() and self.par_dict[key - 1]["par"][0].isdigit():
                self.par_dict[key]["tag"] = self._item
            # the link of third party
            elif self._maybeItem(key) and self._calUrl(text) > 0.5:
                self.par_dict[key]["tag"] = self._item

##################################################################################################
            if (not text[0].isalnum()) and (last[0] == text[0] or next[0] == text[0]) and (text[:2] != "[@"):

                self.par_dict[key]["tag"] = self._item
            elif text[:3].lower () == "to " and (last[:3] == text[:3] or next[:3] == text[:3]):
                self.par_dict[key]["tag"] = self._item
            elif text[:8].lower() == "request " and (last[:8] == text[:8] or next[:8] == text[:8]):
                self.par_dict[key]["tag"] = self._item
            elif text.endswith (self.theEndofStr):
                self.par_dict[key]["tag"] = self._item
                if key + 1 != len (self.par_dict):
                    self.par_dict[key + 1]["tag"] = self._item

            # the link of third party
            elif self._calUrl (text) > 0.5 and (self._calUrl(last) > 0.5 or self._calUrl(next) > 0.5):
                self.par_dict[key]["tag"] = self._item

    def _getLastItem(self, key):
        return self.par_dict[key - 1]["par"].strip() \
            if key != 0 and len(self.par_dict[key - 1]["par"].strip()) > 0 else "null"

    def _getNextItem(self, key):
        return self.par_dict[key + 1]["par"].strip() \
            if key+1 != len(self.par_dict) and len(self.par_dict[key + 1]["par"].strip()) else "null"

    def _maybeItem(self, key, notNULL=True):
        if notNULL:
            maybe = key != 0 and self.par_dict[key - 1]["tag"] != self._unTAG and len(self.par_dict[key]["par"].strip()) > 0
        else:
            maybe = key != 0 and self.par_dict[key - 1]["tag"] != self._unTAG and len(self.par_dict[key]["par"].strip()) == 0
        return maybe

    def _isStart(self, key):
        paragraph = self.par_dict[key]["par"].strip()
        return True if (len(paragraph.strip()) > 0 and paragraph.strip()[-1] == ":") else False

    @staticmethod
    def _calUrl(text):
        max_url_ken = 0
        if len(text.strip()) > 0:
            for i in text.split(" "):
                url = re.search(urlReg, i)
                if url and len(url.group()) / len(text) > max_url_ken:
                    max_url_ken = len(url.group()) / len(text)
        return max_url_ken

    @property
    def mergeBMESPair(self):
        if self.isBMES:
            for key, item in enumerate(self.par_dict):
                if item["tag"] == self._unTAG or item["tag"] == self._start:
                    self._merged_par.append({"par": item["par"], "label": item["label"]})
                else:
                    self._merged_par[-1]["par"] += item["par"]
        else:
            for key, item in enumerate(self.par_dict):
                if item["tag"] == self._unTAG or item["tag"] == self._start:
                    self._merged_par.append({"par": item["par"], "label": "None"})
                else:
                    self._merged_par[-1]["par"] += item["par"]
        return self._merged_par

    @property
    def merge(self):
        result = []
        for key, item in enumerate(self.par_dict):

            if item["tag"] == self._unTAG or item["tag"] == self._start:
                result.append([item["par"]])
            else:
                if self.par_dict[key - 1]["tag"] == self._unTAG or key == 0:
                    result.append ([])
                try:
                    result[-1].append (item["par"])
                except:
                    pass

        return result


def check_have_ul_merge(text):
    if re.search(r"\[@Start#\]", text) is None:
        return False
    else:
        return True



