from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter

from streamparse.bolt import Bolt


class Logger(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        words = tup.values[0]
        at_user = words["user"]["screen_name"]
        display_name = words["user"]["name"].title()
        user_location = words["user"]["location"].title()
        user_image = words["user"]["profile_image_url"]
        text = words["text"]

        tweet = "\n\n@%s (%s)\n\tLocation: %s\n\tImage url: %s\n\nStatus:\n%s" % (at_user,display_name,user_location,user_image,text)
        self.log(tweet)
