#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from __future__ import absolute_import, print_function, unicode_literals

from streamparse.spout import Spout
from twitter import *


class TweetSpout(Spout):
    def initialize(self, stormconf, context):
        self.CONSUMER_KEY = ""
        self.CONSUMER_SECRET = ""
        self.TOKEN_KEY = ""
        self.TOKEN_SECRET = ""

        self.get_keys()
        self.log("\n\n Got keys \n\n")

        self.auth = OAuth(self.TOKEN_KEY, self.TOKEN_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.log("\n\n Got Oauth \n\n")

        self.generate_tweet_pool()

    def generate_tweet_pool(self):
        twitter_stream = TwitterStream(auth=self.auth)
        self.log("\n\n Got Stream \n\n")

        self.tweets = twitter_stream.statuses.sample()
        self.log("\n\n Got Iterator \n\n")

    def get_keys(self):
        with open("keys.rsa", "r") as f:
            self.CONSUMER_KEY = f.readline()
            self.log("\n\n Key: %s \n\n" % (self.CONSUMER_KEY))

            self.CONSUMER_SECRET = f.readline()
            self.log("\n\n Key: %s \n\n" % (self.CONSUMER_SECRET))

            self.TOKEN_KEY = f.readline()
            self.log("\n\n Key: %s \n\n" % (self.TOKEN_KEY))

            self.TOKEN_SECRET = f.readline()
            self.log("\n\n Key: %s \n\n" % (self.TOKEN_SECRET))

    def next_tuple(self):
        while True:
            try:
                tweet_to_emit = self.tweets.next()
                self.emit([tweet_to_emit])
                break

            except Exception, e:
                self.log("Error: %s" % (e.message))
                self.generate_tweet_pool()
