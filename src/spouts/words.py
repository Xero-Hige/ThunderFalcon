from __future__ import absolute_import, print_function, unicode_literals

import itertools
import os
from streamparse.spout import Spout

class WordSpout(Spout):

    def initialize(self, stormconf, context):
	words = [x for x in os.listdir("./tweets") if ".log" in x]
	words.sort()
	self.words = itertools.cycle(words)

    def next_tuple(self):
        word = next(self.words)
        self.emit([word])
