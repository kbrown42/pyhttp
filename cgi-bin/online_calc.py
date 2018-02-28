#!/usr/bin/env python

import sys
from code import compile_command


expr = sys.argv[1]
result = ''
output = ''
try:
    code_object = compile_command(expr, '<string>', 'eval')
    result = eval(code_object)
    if result is not None:
        output = f"""
            <html>
            <body>
            <h2> {expr} = {result}</h2>
            </body>
            </html>
        """
    else:
        output = f"""
            <html>
            <body>
            <h2> Your expression: {expr}\nis incomplete</h2>
            </body>
            </html>
        """

except (SyntaxError, ValueError):
    output = f"""
        <html>
        <body>
        <h2> Could not run your expression: {expr}</h2>
        </body>
        </html>
        """

print(output)
