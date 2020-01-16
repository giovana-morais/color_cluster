import os
import logging
import pickle as pkl

def load_file(file):
    logging.info("Loading file {}".format(os.path.basename(file)))
    with open(file, 'rb') as f:
        data = pkl.load(f)
    return data

def save_file(file, n_clusters, data):
    logging.info("Saving file {}".format(os.path.basename(file)))
    with open(file, 'wb') as f:
        pkl.dump(data, f)

