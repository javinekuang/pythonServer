import os
import json

d = dict(name='Bob', age=20, score=88)
d1 = dict(name='Jak', age=19, score=97)

#with open('dump.txt', 'wb') as f:
 #   f.write(json.dumps(d))
  #  f.write(json.dumps(d1))

with open('dump.txt', 'rb') as f:
    x = f.read()