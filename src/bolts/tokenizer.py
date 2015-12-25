from __future__ import absolute_import, print_function, unicode_literals

from streamparse.bolt import Bolt


class Tokenizer(Bolt):
    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        tweet_dict = tup.values[0]
        values = {}

        values["at_user"] = tweet_dict["user"]["screen_name"]
        values["display_name"] = tweet_dict["user"]["name"].title()
        values["user_location"] = tweet_dict["user"]["location"]
        values["user_image"] = tweet_dict["user"]["profile_image_url"].replace("_normal.jpg", ".jpg")
        values["user_back"] = tweet_dict["user"].get("profile_banner_url", " ")

        self.emit([values])
