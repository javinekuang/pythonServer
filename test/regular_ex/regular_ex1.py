__author__ = 'Administrator'

import re

print 'please input something...'
test = raw_input()
if re.match(r'^\d{3}[a-zA-Z\_\s]*\-\d{3,8}$',test):
    print 'ok'
else:
    print 'failed'

m = re.match(r'^(\d{3})-(\d{3,8})$',test)
print m