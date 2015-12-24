from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter

from streamparse.bolt import Bolt


class Tokenizer(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        tweet = tup.values[0]
        words = tweet.split()
        self.emit([words])