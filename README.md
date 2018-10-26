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

hide(path=image path that will store image inside it,s_path=image to hide,n_path=path to store new image)
show(image=image path which has image image inside it,path=image path to store extracted image)
