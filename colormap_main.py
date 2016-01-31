import os
from matplotlib import pyplot

from scipy.ndimage import imread
from skimage.io import imshow, show
from colormap import spaces, mappers, expressions
from numpy import ones, array, hstack, zeros

# Obtenemos imagen RGB
from colormap.expressions import IN
from colormap.spaces import hsv

rgb_img = spaces.rgb_normalize(imread(os.path.join(os.path.dirname(__file__), 'source.png'), mode='RGBA'))


def lower_blue(a):
    return a * (1, 1, 0.5, 1)

mapper1 = mappers.Mapper()
mapper1.on(lambda hsv: hsv.h_is(IN(0, 3./180.0)) | hsv.h_is(IN(177.0/180.0, 1)), spaces.hsv).do(
    lower_blue, spaces.rgb  # disminuir azul a la mitad cuando el matiz sea rojo
)


mapped_img = mapper1.run(rgb_img, True)

plot = imshow(mapped_img)
show()
