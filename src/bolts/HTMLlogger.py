from __future__ import absolute_import, print_function, unicode_literals

import codecs

from streamparse.bolt import Bolt

HTML_HEADER = """<html>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
    <link href="http://codegena.com/assets/css/image-preview-for-link.css" rel="stylesheet">
    <script type="text/javascript">
        $(function() {
            $('#p1 a').miniPreview({ prefetch: 'pageload' });
            $('#p2 a').miniPreview({ prefetch: 'parenthover' });
            $('#p3 a').miniPreview({ prefetch: 'none' });
        });
    </script>
    <script src="http://codegena.com/assets/js/image-preview-for-link.js"></script>

	<head>
	<meta charset="UTF-8">
	<title>Output</title>
	</head>

	<style type="text/css">
        #rcorners2 {
            border-radius: 25px;
            border: 2px solid #73AD21;
            padding-top: 5px;
            padding-right: 5px;
            padding-bottom: 5px;
            padding-left: 15px;
            width: 580px;
            height: 190px;
            margin: auto auto;
            color:  #0000e3;
            background-color: rgb(192, 222, 237);
            background-color: rgba(192, 222, 237, 0.7);
        }

        #rcorners3 {
            background-size:cover;
            border: 2px solid #1dcaff;
            border-radius: 25px;
            background-position: center center;
            background-repeat: no-repeat;
            padding-top: 20px;
            padding-right: 20px;
            padding-bottom: 20px;
            padding-left: 20px;
            width: 620px;
            height: 220px;
            margin: auto auto;

        }
    </style>"""

class Logger(Bolt):
    def initialize(self, conf, ctx):
        self.count = 0
	with codecs.open('/var/www/html/out.html', encoding='utf-8', mode='w') as f:
            f.write(HTML_HEADER)

    def process(self, tup):
        tweet = tup.values[0]

        try:
            with codecs.open('/var/www/html/out.html', encoding='utf-8', mode='a') as f:
                f.write(tweet)
		self.count += 1
		self.log("Count: "+str(self.count))
        except Exception, e:
            self.log("Error: %s" % (e.message))
            return  # FIXME
