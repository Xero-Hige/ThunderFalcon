from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter

from streamparse.bolt import Bolt


class WorldCounter(Bolt):
    def initialize(self, conf, ctx):
        self.counts = Counter()

    # noinspection PyTypeChecker
    def process(self, tup):
        word = tup.values[0]
        self.counts[word] += 1
        self.emit([word, self.counts[word]])
        self.log('%s: %d' % (word, self.counts[word]))
