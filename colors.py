import os
import math
import logging
import numpy as np
import pickle as pkl

from PIL import Image
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def distance(x, y, alg="euclidian"):
    (rx, gx, bx) = x
    (ry, gy, by) = y
    if alg == "euclidian":
        dist = math.sqrt((rx-ry)**2 + (gx-gy)**2 + (bx-by)**2)
    elif alg == "manhattan":
        dist = np.abs(rx-ry) + np.abs(gx-gy) + np.abs(bx-by)
    return dist

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

    # returns a list and each item of it is a tuple (r, g, b)
    pixels = list(img.getdata())

    basic_colors = list(colors.keys())
    logging.debug("basic_colors", basic_colors)

    for point in pixels:
        closest_colors = sorted(colors, key=lambda color: distance(color, point))
        closest_color = closest_colors[0]
        colors[closest_color] += 1

    logging.debug(colors)
    return colors

def get_colors(image, n_colors=3, method="kmeans"):
    color_clusters = None
    if method == "kmeans":
        color_clusters = get_colors_kmeans(image, n_colors)
    elif method == "quantization":
        color_clusters = get_colors_quantization(image, n_colors)
    else:
        raise ValueError("Unknow method")

    return color_clusters

def get_colors_kmeans(image, n_clusters=3, resize_method="bilinear", new_size=(200,200), save=False):
    pkl_file = image.split('.')[0] + "_{}.pickle".format(n_clusters)

    if os.path.isfile(pkl_file):
        centroids = load_file(pkl_file)
    else:
        img = Image.open(image)
        method = {"nearest": Image.NEAREST,
                  "bilinear": Image.BILINEAR,
                  "bicubic": Image.BICUBIC,
                  "lanczos": Image.LANCZOS}

        resized = img.resize(new_size, method.get(resize_method))
        data = np.asarray(resized)
        r, g, b = data[:,:,0].flatten(), data[:,:,1].flatten(), data[:,:,2].flatten()

        pixels = np.asarray(resized.getdata())

        color_cluster = KMeans(n_clusters, init='random').fit(pixels)
        centroids = color_cluster.cluster_centers_
        logging.debug(color_cluster.cluster_centers_)
        logging.debug(color_cluster.labels_)

        if save:
            save_file(pkl_file, centroids)
    return centroids

def get_image_clusters(image_centroids, n_clusters=3):
    logging.info("Grouping similar images")
    print(image_centroids[0].shape)
    image_clusters = KMeans(n_clusters).fit(image_centroids)
    logging.debug(image_clusters.cluster_centers_)
    return image_clusters

def get_colors_similarity(img_1, img_2):
    dist_array = np.empty(img_1.shape[0])

    for idx, value in enumerate(img_1.shape[0]):
        dist_array[idx] = distance(img_1[idx], img_2[idx])

    return dist_array

def load_file(file):
    logging.info("Loading file {}".format(os.path.basename(file)))
    with open(file, 'rb') as f:
        data = pkl.load(f)
    return data

def save_file(file, data):
    logging.info("Saving file {}".format(os.path.basename(file)))
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

    logging.debug("RGB: {}".format(rgb))
    logging.debug("HEX {}".format(hex))
    return hex
