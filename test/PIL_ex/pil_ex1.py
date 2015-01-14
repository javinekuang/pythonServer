__author__ = 'Administrator'

import Image, ImageFilter

im = Image.open('..\six.png')

im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.png','png')
