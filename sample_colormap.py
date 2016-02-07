import os
from matplotlib import pyplot

from scipy.ndimage import imread
from skimage.io import imshow, show
from colormap import spaces, mappers
from colormap.types import IN
from colormap.sources import hsv, rgb
from numpy import hstack

# Obtenemos imagen RGB
rgb_img = spaces.rgb_normalize(imread(os.path.join(os.path.dirname(__file__), 'source.png'), mode='RGBA'))

mapper1 = mappers.Mapper()

# Cuando el matiz parezca ser rojo...
mapper1.on(hsv.h_is(IN(0, 3./180.0)) | hsv.h_is(IN(177.0/180.0, 1)), spaces.hsv).do(
    rgb.mul(spaces.rgb.B, 0.5), spaces.rgb  # disminuir azul a la mitad
)

mapped_img = mapper1.run(rgb_img, True)


compared = hstack((rgb_img, mapped_img))


plot = imshow(compared)
show()
