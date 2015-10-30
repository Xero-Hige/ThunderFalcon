from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import json

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

    def process(self, tup):
        word = tup.values[0]
        #self.counts[word] += 1
        line = json.loads(word)
	self.emit([1,word])
        self.log('%s' % (line["user"]["name"]))
