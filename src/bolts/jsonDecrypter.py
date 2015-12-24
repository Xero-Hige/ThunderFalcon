from __future__ import absolute_import, print_function, unicode_literals

import json

from streamparse.bolt import Bolt


class JsonDecrypter(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        tweet = tup.values[0]
        try:
            obj = json.loads(tweet)
        except Exception, e:
            self.log('%s: %s' % ("Error: ", e.message))
            return

        self.emit([obj])
