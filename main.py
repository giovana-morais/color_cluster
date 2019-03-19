import os
import sys
import time
import logging

from PIL import Image

from colors import *
from hist import *

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

FILE = sys.argv[1]

if os.path.isfile(FILE):
    logging.debug("Parâmetro é um arquivo")
    if not os.path.isabs(FILE):
        FILE = os.path.join(os.getcwd(), FILE)
    #img = Image.open(FILE)
    cluster = get_colors(FILE, n_clusters=5)
    print(cluster)
    show_colors(cluster)
    
elif os.path.isdir(FILE):
    imgs = []
    clusters = []
    
    logging.debug("Parâmetro é um diretório")
    if not os.path.isabs(FILE):
        FILE = os.path.join(os.getcwd(), FILE)
    for root, dirs, files in os.walk(FILE):
        for i in files:
            tmp = {}
            tmp['id'] = os.path.join(root, i)
            tmp['clusters'] = get_colors(os.path.join(root, i), n_clusters= 5)
            imgs.append(tmp)
            clusters.append(tmp['clusters'])

    get_image_clusters(clusters)
#    get_indexes(clusters)

    logging.debug(clusters)
    


"""
print("Calculando distância com o kmeans")
init = time.time()
clusters = get_colors(nearest, 5)
print("Tempo de execução: {}".format(time.time()-init))

show_color(clusters)
#img.show()


Modo 1: só a pasta de imagens é passada
Gera os arquivos com todos os centróides e depois os agrupa por similaridade
É um kmeans seguido de um kmeans

Modo 2: uma imagem é passada
Gera os centroides da imagem. Se tiver uma pasta de imagens, separa as imagens mais parecida
com a entrada. 

Modo 3: uma ou mais cores são passadas
Gera as imagens e compara com a cor em questão

"""
