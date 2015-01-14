__author__ = 'Administrator'

import re

print 'Please Input your Email Address:'
e = raw_input()

m = re.match(r'^([0-9a-zA-Z\_\.]+)\@([0-9a-zA-Z\.\_]+)\.(com|cn|org)',e)
if m!=None:
    print m.group(1)
else:
    print 'match failed!!'