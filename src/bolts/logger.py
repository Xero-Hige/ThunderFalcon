from __future__ import absolute_import, print_function, unicode_literals

from streamparse.bolt import Bolt

from string import Template

HTML_TEMPLATE = """<html>
	<head>
		<title></title>
	</head>
	<body>
		<div id="rcorners3">
			<div id="rcorners2">
				<p>
					<a href="$profile_pic"><img alt="" src="$profile_pic" style="width: 100px; height: 100px; float: left;" /></a></p>
				<p>
					&nbsp;<strong>@$user</strong> (<em>$name</em>)</p>
				<p>
					From: <u>$location</u></p>
				<p>
					$text
				<p>
					&nbsp;</p>
				<p>
					&nbsp;</p>
			</div>
		</div>
		<p>
			&nbsp;</p>
		<style type="text/css">
#rcorners2 {
    border-radius: 25px;
    border: 2px solid #73AD21;
    background: #c0deed;
    padding-top: 5px;
    padding-right: 5px;
    padding-bottom: 5px;
    padding-left: 15px;
    width: 580px;
    height: 190px;
    margin: auto auto;
color:  #0084b4;
}

#rcorners3 {
    border-radius: 25px;
    background: url($header);
    background-position: left top;
    background-repeat: repeat;
    padding-top: 20px;
    padding-right: 20px;
    padding-bottom: 20px;
    padding-left: 20px;
    width: 620px;
    height: 220px;
}		</style>
	</body>
</html>"""

class Logger(Bolt):
    def initialize(self, conf, ctx):
        self.tweet_template = Template(HTML_TEMPLATE)

    def process(self, tup):
        words = tup.values[0]

        if not words:
            return

        at_user = words["user"]["screen_name"]
        display_name = words["user"]["name"].title()
        user_location = words["user"]["location"]
        user_image = words["user"]["profile_image_url"].replace("_normal.jpg",".jpg")
        user_back = words["user"]["profile_banner_url"]

        text = words["text"]

        tweet = self.tweet_template.substitute(profile_pic=user_image,user=at_user,name=display_name,header=user_back,text=text,location=user_location)
        try:
            #tweet = tweet.decode('unicode-escape')
            with open('/var/www/html/out.html', 'a') as f:
                f.write(tweet)
        except:
            return  # FIXME
        #self.log(tweet)
