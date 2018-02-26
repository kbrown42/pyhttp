#!/usr/bin/env python2.7
import sys, os

info = os.popen('uptime').read()


print """\
<html>
<body>
<h2>Server up time:<br> {}</h2>
</body>
</html>
""".format(info)
