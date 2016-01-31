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

    Even if it is not allowed to cache, will store the last processing result.
    """

    def __new__(cls, image, cache):
        value = super(MappingContext, cls).__new__(image, {} if cache else None)
        value.__colorspace = rgb
        value._set_last(None, None)
        return value

    def _set_last(self, space, image):
        self.__last_image = image
        self.__last_space = space
        return image

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

        If the requested format is rgb we return the initial image.
        If the requested format is the same last format, we return the same last image.
        Otherwise we compute it or recover it from cache, according to the case.
        """

        if not isinstance(rgb, ColorSpace):
            raise TypeError("process_image() expects a single parameter of type ColorSpace")

        if colorspace == rgb:
            return self.image

        if colorspace == self.__last_space:
            return self.__last_image

        if self.cache is None:
            return self._set_last(colorspace, colorspace.encoder(self.image))
        else:
            if colorspace not in self.cache:
                self.cache[colorspace] = self._set_last(colorspace, colorspace.encoder(self.image))
            return self.cache[colorspace]


class Masker(collections.namedtuple('Masker', ('masker', 'colorspace'))):
    """
    A masker is a function executed with a colorspace.
    Takes a function, and a colorspace, to process an image in a mapping context.
    """

    def __new__(cls, masker, colorspace=rgb):
        return super(Masker, cls).__new__(cls, masker, colorspace)

    def get_mask(self, context):
        return self.masker(context.process_image(self.colorspace))
