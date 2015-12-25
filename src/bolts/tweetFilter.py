from __future__ import absolute_import, print_function, unicode_literals

from streamparse.bolt import Bolt


class Filter(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        tweet = tup.values[0]
        try:
            if "coordinates" in tweet and tweet["coordinates"]:
                self.emit([tweet])  # FIXME


            elif "geo" in tweet and tweet["geo"]:
                self.emit([tweet])  # FIXME


            elif "place" in tweet and tweet["place"]:
                self.emit([tweet])  # FIXME

        except Exception, e:
            self.log("Error: %s" % (e.message))
