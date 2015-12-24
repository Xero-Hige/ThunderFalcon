from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter

from streamparse.bolt import Bolt


class Logger(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        words = tup.values[0]
        self.log(words.keys())
