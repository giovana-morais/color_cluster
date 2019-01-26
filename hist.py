import matplotlib.pyplot as plt

def get_hist(img):
    hist = img.histogram()

    r_hist = hist[0:256]
    g_hist = hist[256:512]
    b_hist = hist[512::]

    # plotar os histogramas separados não vai dar uma noção mt boa do que tá
    # acontecendo em um panorama geral, mas é um começo pra enxergar as camadas
    # da imagem
    plt.figure(0)
    for i in range(0, 256):
        #plt.bar(i, r_hist[i], color=get_red(i), alpha=0.3)
        plt.bar(i, r_hist[i], alpha=0.3)

    plt.figure(1)
    for i in range(0, 256):
        #plt.bar(i, g_hist[i], color=get_green(i), alpha=0.3)
        plt.bar(i, g_hist[i], alpha=0.3)

    plt.figure(2)
    for i in range(0, 256):
        #plt.bar(i, b_hist[i], color=get_blue(i), alpha=0.3)
        plt.bar(i, b_hist[i], alpha=0.3)
   
    plt.show()
