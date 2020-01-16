import os
import sys
import time
import logging

from PIL import Image

from colors import *
from hist import *

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

FILE = sys.argv[1]
N_COLORS = int(sys.argv[2])

if os.path.isfile(FILE):
    logging.debug("Argument is a file")
    if not os.path.isabs(FILE):
        FILE = os.path.join(os.getcwd(), FILE)
    cluster = get_colors(FILE, n_colors=N_COLORS, save=True)
    print(cluster)
    show_colors(cluster)
elif os.path.isdir(FILE):
    imgs = []
    clusters = []

    logging.debug("Argument is a folder")
    if not os.path.isabs(FILE):
        FILE = os.path.join(os.getcwd(), FILE)
    for root, dirs, files in os.walk(FILE):
        if_ = True
        for i in files:
            tmp = {}
            tmp['id'] = os.path.join(root, i)
            tmp['clusters'] = get_colors(os.path.join(root, i), n_colors=N_COLORS)
            imgs.append(tmp)
            clusters.append(tmp['clusters'])


    logging.debug("GET IMAGE CLUSTERS")
    logging.debug(clusters)
    get_image_clusters(clusters)
#    get_indexes(clusters)

    logging.debug(clusters)
