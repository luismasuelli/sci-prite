import collections


ColorSpace = collections.namedtuple('ColorSpace', ['key', 'encoder', 'decoder'])


def is_colorspace(cs):
    return cs is None or cs == current


from skimage.color import (
    rgb2hsv, hsv2rgb,
    rgb2luv, luv2rgb,
    rgb2hed, hed2rgb,
    rgb2lab, lab2rgb,
    rgb2xyz, xyz2rgb,
)


current = ColorSpace(None, None)
rgb = ColorSpace(lambda a: a, lambda a: a)
hsv = ColorSpace(rgb2hsv, hsv2rgb)
luv = ColorSpace(rgb2luv, luv2rgb)
hed = ColorSpace(rgb2hed, hed2rgb)
lab = ColorSpace(rgb2lab, lab2rgb)
xyz = ColorSpace(rgb2xyz, xyz2rgb)


class ColorSpaceWrapper(object):
    """
    This is just a wrapper for an array describing an image.
    Any operation sent to this object, other than the specifically implemented
      in this object (or any subclass) goes directly to the wrapped object.
    """

    def __init__(self, np_image):
        self.__np_image = np_image

    @property
    def np_image(self):
        """
        Returns the wrapped object.
        """

        return self.__np_image

    # Other calls are simply proxied.

    def __setattr__(self, key, value):
        return setattr(self.__np_image, key, value)

    def __getattr__(self, item):
        return getattr(self.__np_image, item)


def band_property(idx):
    """
    Creates a band property for the space. e.g.

    r, g, b,
    h, s, v,
    l, a, b,

    All of them would be implemented like this.
    :param idx:
    :return:
    """

    def _get(self):
        return self.np_image[:, :, idx]

    def _set(self, value):
        self.np_image[:, :, idx] = value

    return property(_get, _set)


def band_properties(cnt):
    """
    Intended to be used on classes. This creates one property for each band in the intended
      amount of bands.

    E.g.

      r, g, b, a = band_properties(4)
    """

    return tuple(band_property(k) for k in range(cnt))


class RGB(ColorSpaceWrapper):
    """
    RGB (perhaps with Alpha) color space.
    """

    r, g, b, alpha = band_properties(4)


class HSV(ColorSpaceWrapper):
    """
    HSV (perhaps with Alpha) color space.
    """

    h, s, v, alpha = band_properties(4)


class LUV(ColorSpaceWrapper):
    """
    LUV (perhaps with Alpha) color space.
    """

    l, u, v, alpha = band_properties(4)


class HED(ColorSpaceWrapper):
    """
    HED (perhaps with Alpha) color space.
    """

    h, e, d, alpha = band_properties(4)


class LAB(ColorSpaceWrapper):
    """
    LAB (perhaps with Alpha) color space.
    """

    l, a, b, alpha = band_properties(4)


class XYZ(ColorSpaceWrapper):
    """
    XYZ (perhaps with alpha) color space.
    """

    x, y, z, alpha = band_properties(4)