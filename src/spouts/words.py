from __future__ import absolute_import, print_function, unicode_literals

import itertools
import os
from streamparse.spout import Spout

class WordSpout(Spout):

    def initialize(self, stormconf, context):
	words = ["./tweets/"+x for x in os.listdir("./tweets") if ".log" in x]
	words.sort()
	self.words = itertools.cycle(words)
	self.file = open(next(self.words))

    def next_tuple(self):
	line = self.file.readline()
	while (not line):
		self.file.close()
		self.file = open(next(self.words))
		line = self.file.readline()
	self.emit([line])
