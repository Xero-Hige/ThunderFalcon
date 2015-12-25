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

        self.auth = OAuth(self.TOKEN_KEY, self.TOKEN_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET)

        self.generate_tweet_pool()

    def generate_tweet_pool(self):
        twitter_stream = TwitterStream(auth=self.auth)
        self.tweets = twitter_stream.statuses.sample()

    def get_keys(self):
        with open("keys.rsa", "r") as f:
            self.CONSUMER_KEY = f.readline()
            self.CONSUMER_SECRET = f.readline()
            self.TOKEN_KEY = f.readline()
            self.TOKEN_SECRET = f.readline()

    def next_tuple(self):
        tweet_to_emit = None
        while not tweet_to_emit:
            try:
                tweet_to_emit = self.tweets.next()
            except Exception, e:
                self.log("Error: %s" % (e.message))
                self.generate_tweet_pool()

        self.emit([tweet_to_emit])
