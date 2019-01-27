import os
import sys
import time

from PIL import Image

from colors import *
from hist import *

FILE = sys.argv[1]

if os.path.isfile(FILE):
    print("Parâmetro é um arquivo")
    if not os.path.isabs(FILE):
        FILE = os.path.join(os.getcwd(), FILE)
    #img = Image.open(FILE)
    cluster = get_clusters(FILE, n_clusters=5)
    print(cluster)
    show_colors(cluster)

    
elif os.path.isdir(FILE):
    clusters = []
    
    print("Parâmetro é um diretório")
    if not os.path.isabs(FILE):
        FILE = os.path.join(os.getcwd(), FILE)
    for root, dirs, files in os.walk(FILE):
        for i in files:
            tmp = {}
            tmp['id'] = os.path.join(root, i)
            tmp['clusters'] = get_clusters(os.join(root, i), "nearest", 5)
            clusters.append(tmp)
    

    print(clusters)


"""
print("Calculando distância com o kmeans")
init = time.time()
clusters = get_clusters(nearest, 5)
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
