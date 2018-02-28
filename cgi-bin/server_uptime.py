#!/usr/bin/env python

import os


info = os.popen('uptime').read()


print(f"""\
<html>
<body>
<h2>Server up time:<br> {info}</h2>
</body>
</html>
""")
