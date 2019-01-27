import os
import math
import numpy as np
import pickle as pkl

from PIL import Image
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def get_red(red_val):
    return (red_val, 0, 0)

def get_green(green_val):
    return (0, green_val, 0)

def get_blue(blue_val):
    return (0, 0, blue_val)

def distance(x, y, alg="euclidian"):
    (rx, gx, bx) = x
    (ry, gy, by) = y

    if alg == "euclidian":
        dist = math.sqrt((rx-ry)**2 + (gx-gy)**2 + (bx-by)**2)

    return dist 

# dada uma matriz inicial, faz um agrupamento dos pixels mais próximos 
def get_closest_pixels(img, colors=None):
    if not colors:
        colors = {
                    (255, 0  , 0)   : 0,    # red
                    (255, 127, 0)   : 0,    # orange
                    (255, 255, 0)   : 0,    # yellow
                    (0  , 255, 0)   : 0,    # green
                    (0  , 0  , 255) : 0,    # blue
                    (75 , 0  , 130) : 0,    # purple
                    (143, 0  , 255) : 0     # violet
                  }

    # já retorna uma lista com cada item sendo uma tupla do tipo (r, g, b)
    pixels = list(img.getdata())

    basic_colors = list(colors.keys())
    print("basic_colors", basic_colors)

    for point in pixels:
        closest_colors = sorted(colors, key=lambda color: distance(color, point))
        closest_color = closest_colors[0]
        colors[closest_color] += 1

    print(colors)

def get_clusters(image, n_clusters=3, resize_method="nearest", new_size=(50,50)):
    pkl_file = image.split('.')[0] + ".pickle"

    if os.path.isfile(pkl_file):
        centroids = load_file(pkl_file)
    else:
        img = Image.open(image)

        if resize_method == "nearest":
            resized = img.resize(new_size, Image.NEAREST)
        elif resize_method == "bilinear":
            resized = img.resize(new_size, Image.BILINEAR)
        elif resize_method == "bicubic":
            bicubic = img.resize(new_size, Image.BICUBIC)
        elif resize_method == "lanczos":
            lanczos = img.resize(new_size, Image.LANCZOS)
        else:
            raise(ValueError("{} is a invalid resize method".format(resize_method)))

        pixels = list(resized.getdata())

        color_cluster = KMeans(n_clusters).fit(pixels)
        centroids = color_cluster.cluster_centers_
        print(color_cluster.cluster_centers_)

        save_file(pkl_file, centroids)
    return centroids


def load_file(file):
    print("Carregando arquivo {}".format(os.path.basename(file)))
    with open(file, 'rb') as f:
        data = pkl.load(f)
    return data 


def save_file(file, data):
    print("Salvando arquivo {}".format(os.path.basename(file)))
    with open(file, 'wb') as f:
        pkl.dump(data, f)

def show_colors(rgb):
    bar = 0
    hex = rgb_to_hex(rgb)
    for i in rgb:
        plt.bar(hex[bar], 2, color=hex[bar])
        bar += 1

    plt.show()

def rgb_to_hex(rgb):
    hex = []
    for i in rgb:
        hex.append('#{:02x}{:02x}{:02x}'.format(int(i[0]), int(i[1]), int(i[2])))

    #print("RGB: {}".format(rgb))
    #print("HEX {}".format(hex))
    return hex
