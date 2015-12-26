# coding=utf-8
from __future__ import absolute_import, print_function, unicode_literals

import re
from string import Template

from streamparse.bolt import Bolt

HTML_TEMPLATE = """
	<body>
		<div id="rcorners3" style="background-image: url($header)" >
			<div id="rcorners2">
				<p>
					<a href="$profile_pic"><img alt="" src="$profile_pic" style="width: 100px; height: 100px; float: left;" /></a></p>
				<p>
					&nbsp;<strong>@$user</strong> (<em>$name</em>)</p>
				<p>
					From: <u>$location</u>   <a href=http://www.google.com/maps/place/$latitude,$longitude/@$latitude,$longitude,17z/data=!3m1!1e3>⬤</a> </p>
				<p id="p3">
					$text
				<p>
					&nbsp;</p>
				<p>
					&nbsp;</p>
			</div>
		</div>
		<p>
			&nbsp;</p>
	</body>
"""


class Generator(Bolt):
    def initialize(self, conf, ctx):
        self.tweet_template = Template(HTML_TEMPLATE)

    def process(self, tup):
        tweet_values = tup.values[0]

        at_user = tweet_values["at_user"]
        display_name = tweet_values["display_name"]
        user_location = tweet_values["user_location"]
        user_image = tweet_values["user_image"]
        user_back = tweet_values["user_back"]
        text = tweet_values["text"]
        latitude = tweet_values["latitude"]
        longitude = tweet_values["longitude"]

        text = self.add_link_tags(text)

        tweet = self.tweet_template.substitute(profile_pic=user_image, user=at_user, name=display_name,
                                               header=user_back, text=text, location=user_location, latitude=latitude,
                                               longitude=longitude)

        self.emit([tweet])

    def add_link_tags(self, text):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        for url in urls:
            text = text.replace(url, '<a href="' + url + ' ">' + url + '</a>')
        return text
