import os
import logging
import pickle as pkl
import numpy as np

def load_file(file):
    logging.info("Loading file {}".format(os.path.basename(file)))
    with open(file, 'rb') as f:
        data = pkl.load(f)
    return data

def save_file(file, n_clusters, data):
    logging.info("Saving file {}".format(os.path.basename(file)))
    with open(file, 'wb') as f:
        pkl.dump(data, f)

def compute_label_qty(labels):
    labels_list = np.unique(labels)
    qty = np.empty(labels_list.shape)

    for i in labels_list:
        qty[i] = np.sum(labels == i)

    qty = qty.astype(float)
    qty /= qty.sum()

    return qty

