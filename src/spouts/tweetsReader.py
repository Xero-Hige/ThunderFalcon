from __future__ import absolute_import, print_function, unicode_literals

import itertools
import os

from streamparse.spout import Spout

TWEETS_FOLDER = "/home/hige/ThunderFalcon/tweets"


class TweetSpout(Spout):
    def initialize(self, stormconf, context):
        words = [x for x in os.listdir(TWEETS_FOLDER) if ".log" in x]
        words.sort(reverse=True)
        self.words = itertools.cycle(words)
        self.file = None
        self.open_file()

    def next_tuple(self):
        tweet_to_emit = self.file.readline()

        while not tweet_to_emit:
            self.open_file()
            tweet_to_emit = self.file.readline()

        self.emit([tweet_to_emit])

    def open_file(self):
        try:
            self.file.close()
        except AttributeError:
            pass  # No need to close file

        self.file = None
        while not self.file:
            try:
                filename = self.words.next()

                filepath = os.path.join(TWEETS_FOLDER, filename)
                self.file = open(filepath)
            except:
                continue
