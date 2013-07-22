# import necessary modules
from PIL import Image
import hashlib
import time
import os
import sys

# variations on coordenates
dx = [0,0,1,-1,1,-1,1,-1]
dy = [1,-1,0,0,1,1,-1,-1]

# open the image and create a new one
im = Image.open(sys.argv[1])
im2 = Image.new("P",im.size,255)
im = im.convert("P")
temp = {}

# mantain a pixel if all its neighbors are not so white
for x in range(im.size[1]):
  for y in range(im.size[0]):
    pix = im.getpixel((y,x))

    cnt = 0
    for i in range(8):
      ny = y+dy[i]
      nx = x+dx[i]
      if ny >= 0 and ny < im.size[0] and nx >= 0 and nx < im.size[1] and im.getpixel((ny,nx)) < 100:
        cnt = cnt + 1
    if cnt == 8: # these are the numbers to get
      im2.putpixel((y,x),0)

# save the filtered image
im2.save(sys.argv[2])
sys.exit(0)
