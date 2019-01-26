import math
import numpy as np
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
def get_closest_pixels(img, colors):
    # já retorna uma lista com cada item sendo uma tupla do tipo (r, g, b)
    pixels = list(img.getdata())

    basic_colors = list(colors.keys())
    print("basic_colors", basic_colors)

    for point in pixels:
        closest_colors = sorted(colors, key=lambda color: distance(color, point))
        closest_color = closest_colors[0]
        colors[closest_color] += 1

    print(colors)

def get_clusters(img):
    n_clusters = 10 
    pixels = list(img.getdata())

    color_cluster = KMeans(n_clusters).fit(pixels)
    print(color_cluster.cluster_centers_)
    return color_cluster.cluster_centers_


def show_color(rgb):
    bar = 0
    hex = rgb_to_hex(rgb)
    for i in rgb:
        plt.bar(bar, 2, color=hex[bar])
        bar += 1

    plt.show()

def rgb_to_hex(rgb):
    hex = []
    print("RGB: {}".format(rgb))
    for i in rgb:
        hex.append('#{:02x}{:02x}{:02x}'.format(int(i[0]), int(i[1]), int(i[2])))

    print("HEX {}".format(hex))
    return hex
