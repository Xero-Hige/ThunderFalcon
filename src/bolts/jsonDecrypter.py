from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter

from streamparse.bolt import Bolt

import json


class JsonDecrypter(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        tweet = tup.values[0]
        try:
            obj = json.loads(tweet)
        except:
            return

        self.emit([obj])