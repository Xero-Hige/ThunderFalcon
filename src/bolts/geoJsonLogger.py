from __future__ import absolute_import, print_function, unicode_literals

import codecs

from streamparse.bolt import Bolt


class Logger(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        tweet = tup.values[0]

        try:
            with codecs.open('/var/www/html/example/out.html', encoding='utf-8', mode='w') as f:
                f.write(tweet)

        except Exception, e:
            self.log("Error: %s" % (e.message))
            return  # FIXME
