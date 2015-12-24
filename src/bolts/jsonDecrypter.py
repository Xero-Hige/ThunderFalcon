from __future__ import absolute_import, print_function, unicode_literals

import json
import re


from streamparse.bolt import Bolt


class JsonDecrypter(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        tweet = tup.values[0]

        #Replace python values with json valid values
        tweet = tweet.replace("': False","': false")
        tweet = tweet.replace("': True","': true")
        tweet = tweet.replace("': None","': null")

        #Removed unicode "u" since it can not be decrypted
        tweet = tweet.replace("u'",'"')

        #Replaced ' with "
        tweet = tweet.replace("'",'"')

        tweet = re.sub("<a href[^>]*>","<a>",tweet)

        tweet = tweet.decode('unicode-escape')

        self.log("\n\n\n\n%s:\n\n %s\n\n\n\n" % ("tweet: ", tweet))


        try:
            obj = json.loads(tweet)
        except Exception, e:
            self.log('%s: %s' % ("Error: ", e.message))
            return

        self.emit([obj])
