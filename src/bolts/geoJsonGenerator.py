# coding=utf-8
from __future__ import absolute_import, print_function, unicode_literals

import re
from string import Template

from streamparse.bolt import Bolt

GEOJSON_TEMPLATE = """
{
	"geometry": {
		"type": "Point",
		"coordinates": [$longitude, $latitude]
	},
	"type": "Feature",
	"properties": {
		"Text": "@$user:\n$text"
	}
}"""


class Generator(Bolt):
    def initialize(self, conf, ctx):
        self.tweet_template = Template(GEOJSON_TEMPLATE)

    def process(self, tup):
        tweet_values = tup.values[0]

        at_user = tweet_values["at_user"]
        text = tweet_values["text"]
        latitude = tweet_values["latitude"]
        longitude = tweet_values["longitude"]

        text = self.add_link_tags(text)

        tweet = self.tweet_template.substitute(user=at_user, text=text, latitude=latitude,
                                               longitude=longitude)

        self.emit([tweet])

    def add_link_tags(self, text):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        for url in urls:
            text = text.replace(url, '<a href="' + url + ' ">' + url + '</a>')
        return text
