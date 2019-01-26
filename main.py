import sys
import time

from PIL import Image

from colors import *
from hist import *


file = sys.argv[1]
img = Image.open(file)

# tabela básica com as cores do arco íris pro primeiro cálculo de distância.
# vai ser modificada depois pq vai ser gerada a partir da entrada
colors = {
            (255, 0  , 0)   : 0,    # red
            (255, 127, 0)   : 0,    # orange
            (255, 255, 0)   : 0,    # yellow
            (0  , 255, 0)   : 0,    # green
            (0  , 0  , 255) : 0,    # blue
            (75 , 0  , 130) : 0,    # purple
            (143, 0  , 255) : 0     # violet
          }


"""
print("Calculando distância na mão")
init = time.time()
get_closest_pixels(img, colors)
print("Tempo de execução: {}".format(time.time()-init))
"""

print("Calculando distância com o kmeans")
init = time.time()
clusters = get_clusters(img)
print("Tempo de execução: {}".format(time.time()-init))

show_color(clusters)
#img.show()

