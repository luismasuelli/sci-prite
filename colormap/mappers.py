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

    Another use is in a masked-chunk level. In this case, the initial rgb image
      is not the full one, but just a chunk determined by a formerly-existent
      mask. The usage, however, is the same.
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
    A masker is a function executed with a colorspace (by default rgb).
    Takes a function, and a colorspace, to process an image in a mapping context.
    """

    def __new__(cls, masker, colorspace=rgb):
        if not isinstance(rgb, ColorSpace):
            raise TypeError("`colorspace` parameter for Masker must be a ColorSpace instance")
        return super(Masker, cls).__new__(cls, masker, colorspace)

    def get_mask(self, context):
        return self.masker(context.process_image(self.colorspace))


class Action(collections.namedtuple('Action', ('action', 'colorspace'))):
    """
    An action executes over a masked image. For the same masked image, successive
      actions will be applied and, in this way, it's a nonsense to cache the results,
      but only take note on the applied colorspace.
    """

    def __new__(cls, action, colorspace=rgb):
        if not isinstance(rgb, ColorSpace):
            raise TypeError("`colorspace` parameter for Action must be a ColorSpace instance")
        return super(Action, cls).__new__(cls, action, colorspace)

    def execute(self, chunk):
        """
        Executes the action, taking the chunk in RGB[A] and returning it in RGB[A] as well but having
          a specific colorspace for processing.
        :param chunk:
        :return:
        """

        if self.colorspace == rgb:
            return self.action(chunk)
        else:
            return self.colorspace.decoder(self.action(self.colorspace.encoder(chunk)))