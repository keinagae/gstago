import binascii
import numpy as np
from PIL import Image
import os

def bin2str(binary):
    message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
    return message.decode("utf8")


def decode(byte):
    if byte % 10 == 0:
        return ","
    if byte % 2 == 0:
        return 0
    else:
        return 1


def getimgdata(binary):
    binary = str(binary)
    spliter = binary.index("1111111111111111111111111111111111111111")
    binary = binary[:spliter]
    binary = binary.split(",,")
    binary1 = binary[1].split(',')
    raw_pixles=np.array(binary1)
    int_convert = np.vectorize(lambda x: int(x,2))
    flat_pixel = int_convert(raw_pixles)
    img_properties = bin2str(binary[0])
    img_properties = img_properties.split(',')
    img_name = img_properties[0]
    img_mode = img_properties[1]
    img_dimensions = tuple(map(int, img_properties[2:]))
    return img_name, img_mode, img_dimensions, flat_pixel


def str2img(binary,path):
    img_name, img_mode, img_dimensions, img_pixels = getimgdata(binary)
    print(os.path.split(img_name))
    img_pixels.shape=img_dimensions
    nm = Image.fromarray(img_pixels.astype('uint8')).save(os.path.join(path,os.path.split(img_name)[1]))


def show(image,path):
    img = Image.open(image)
    img = img.convert("RGB")
    bin_convert = np.vectorize(lambda l: str(decode(l)))
    np_image=np.array(img).transpose((1,0,-1)).ravel()

    bits_pixel=bin_convert(np_image)
    binary=''.join(map(str,bits_pixel))
    check = str2img(binary,path)


def str2bin(message):
    binary = bin(int(binascii.hexlify(bytes(str(message), "ascii")), 16))
    return binary[2:]


def encode(byte, bit):
    even = 2 * int(int(byte) / 2)
    if bit == "1":
        even = even + 1
    if bit == ",":
        rem = even % 10
        even = even - rem
    elif bit == '0' and even % 10 == 0:
        even = even + 2
    return int(even)


def img2str(path):
    img = Image.open(path)
    np_img=np.array(img)
    shape=','.join(map(str,np_img.shape))
    imageinfo = path + "," + img.mode + "," + shape

    bin_convert = np.vectorize(lambda l:str(bin(l)[2:]))
    flaten_bin_np_img=bin_convert(np_img.ravel())
    imagepixels=','.join(map(str,flaten_bin_np_img))
    binary = str2bin(imageinfo)
    binary = binary + ",," + imagepixels + "1111111111111111111111111111111111111111--"
    return binary

def isvalid2hide(pixels_size, binary_size):
    pixels = pixels_size[0] * pixels_size[1]
    pixels = pixels * 3
    if pixels > binary_size:
        return True
    else:
        return False

def hide(path, s_path,n_path):
    img = Image.open(path)
    img = img.convert("RGB")
    nimg = Image.new(img.mode, img.size)
    pixel_map = img.load()
    npixel_map = nimg.load()
    binary = img2str(s_path)
    current_byte = 0
    if isvalid2hide(img.size, len(binary)):
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                npixel_map[x, y] = pixel_map[x, y]
                if (binary[current_byte] != "-"):
                    pixels = list(npixel_map[x, y])
                    for z in range(len(pixels)):
                        # if binary[current_byte:6] == "1000000" :
                        #   current_byte=current_byte+7
                        if binary[current_byte] != "-":
                            new_byte = encode(pixels[z], binary[current_byte])
                            pixels[z] = new_byte
                            current_byte = current_byte + 1
                        npixel_map[x, y] = tuple(pixels)
                else:
                    pass
        nimg.save(n_path)
    else:
        print("sorry this operation cannot be performed"
              "your secret img is greater then what the "
              "holding img can hide")