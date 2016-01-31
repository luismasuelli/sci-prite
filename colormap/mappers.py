import collections
from numpy import ones, zeros
from .spaces import rgb, ColorSpace


class MappingContext(collections.namedtuple('_MappingContext', ('image', 'cache'))):
    """
    A mapping context relates to an execution of a Map's run() method.
    Involved the following:

    - Referencing the current image.
    - Referencing the current run-wide colorspace.
    - Can calculate and cache elements.
    """

    def __new__(cls, image, cache):
        super(MappingContext, cls).__new__(image, {} if cache else None)

    def __init__(self, image, cache):
        self.__colorspace = rgb

    @property
    def colorspace(self):
        return self.__colorspace

    @colorspace.setter
    def colorspace(self, value):
        if value:
            self.__colorspace = value

    def process_image(self, colorspace):
        """
        Processes (and caches, if applicable) the image.
        """

        if colorspace == rgb:
            return self.image

        if self.cache is None:
            return colorspace.encoder(self.image)
        else:
            if colorspace not in self.cache:
                self.cache[colorspace] = colorspace.encoder(self.image)
            return self.cache[colorspace]