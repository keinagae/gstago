# gstago
Hide an image in other image
You can use it to hide an image inside other

requirements:
numpy
pillow
binascii

example :
in your python file write 
from gstago import show,hide

show function is used to get image from other image and hide is used to hide image

hide(<image path that will store image inside it>,<image to hide>,<path to store new image>)
show(<image path which has image image inside it>,<image path to store extracted image>)
