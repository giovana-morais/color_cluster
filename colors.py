import os
import math
import logging
import numpy as np

from PIL import Image
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import utils
import pdb

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


def get_colors(image, n_clusters=3, resize_method="bilinear", new_size=(200,200), save=False):
    pkl_file = image.split('.')[0] + "_{}.pickle".format(n_clusters)

    if os.path.isfile(pkl_file):
        logging.info("Loading file")
        clusters = utils.load_file(pkl_file)
    else:
        logging.info("Generating palette")
        img = Image.open(image)
        method = {"nearest": Image.NEAREST,
                  "bilinear": Image.BILINEAR,
                  "bicubic": Image.BICUBIC,
                  "lanczos": Image.LANCZOS}

        resized_img = img.resize(new_size, method.get(resize_method))
        data = np.asarray(resized_img)
        r, g, b = data[:,:,0].flatten(), data[:,:,1].flatten(), data[:,:,2].flatten()

        pixels = np.asarray(resized_img.getdata())

        clusters = kmeans(n_clusters, pixels)
        logging.debug(clusters.cluster_centers_)
        logging.debug(clusters.labels_)

        if save:
            utils.save_file(pkl_file, n_clusters, clusters)
    return clusters

def kmeans(n_clusters, pixels):
    return KMeans(n_clusters, init='random').fit(pixels)

def get_cluster_centers(clusters):
    return clusters.cluster_centers_

def get_cluster_members(cluster_id, labels_array):
    return np.where(labels_array == cluster_id)[0]

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

def show_colors(centroids, labels):
    bar = 0
    hex_colors = rgb_to_hex(centroids)
    hex_colors = np.asarray(hex_colors)
    bar_size = utils.compute_label_qty(labels)
    idxs = np.argsort(bar_size)[::-1]

    plt.bar(hex_colors[idxs], bar_size[idxs], color=hex_colors[idxs])
    plt.tight_layout()
    plt.show()

def rgb_to_hex(rgb):
    hex = []
    for i in rgb:
        hex.append('#{:02x}{:02x}{:02x}'.format(int(i[0]), int(i[1]), int(i[2])))

    logging.debug("RGB: {}".format(rgb))
    logging.debug("HEX {}".format(hex))
    return hex
