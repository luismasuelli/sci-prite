from .spaces import rgb, hed, hsv, lab, luv, xyz, current, is_colorspace


class MappingContext(object):
    """
    A mapping context relates to an execution of a Map's run() method.
    Involved the following:

    - Referencing the current image.
    - Referencing the current run-wide colorspace.
    - Can calculate and cache elements.
    """

    def __init__(self, img, caches, colorspace):
        self.__img = img
        self.__caches = caches
        self.__cached = dict()
        self.__colorspace = colorspace

    def caches(self):
        return self.__caches

    def colorspace(self):
        return self.__colorspace

    def process_image(self, colorspace = None):
        """
        Processes (and caches, if applicable) the image.
        """

        if colorspace is None:
            colorspace = self.__colorspace

        if colorspace == rgb:
            return self.__img

        if not self.__caches:
            return colorspace.encoder(self.__img)
        else:
            if colorspace not in self.__cached:
                self.__cached[colorspace] = colorspace.encoder(self.__img)
            return self.__cached[colorspace]