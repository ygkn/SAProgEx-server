#! /usr/bin/env python3
import datetime

# HTTP Header
print("Content-type: text/html\n")

print(
    f"""
<html>
  <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head>
  <body><marquee>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</marquee></body>
</html>
"""
)
