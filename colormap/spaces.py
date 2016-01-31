import collections
from functools import wraps
import numpy

ColorSpace = collections.namedtuple('ColorSpace', ['encoder', 'decoder'])


from skimage.color import (
    rgb2hsv, hsv2rgb,
    rgb2luv, luv2rgb,
    rgb2hed, hed2rgb,
    rgb2lab, lab2rgb,
    rgb2xyz, xyz2rgb,
)


def rgb_normalize(arr):
    """
    Will normalize a uint8 image to a 0..1-valued image.
      Note that alpha channel will also be affected.
    :param arr:
    :return:
    """

    if arr.dtype == numpy.uint8:
        return arr / 255.0
    return arr


def rgb_denormalize(arr):
    """
    Will denormalize a float64 image to a 0..255-valued image.
      Note that alpha channel will also be affected.
    :param arr:
    :return:
    """

    if arr.dtype in (numpy.float32, numpy.float64):
        return arr * 255.0
    return arr


def _alpha_aware_converter(func):
    """
    Returns a new function that will apply the original converter but keep the alpha channel if the image is (W, H, 4).
    :param converter:
    :return:
    """

    @wraps(func)
    def _converter(image):
        if is_4comp(image):
            return numpy.dstack((func(image[:, :, :3]), image[:, :, 3]))
        else:
            return func(image)


def _alpha_aware_colorspace(enc, dec):
    """
    Creates a ColorSpace whose functions are alpha-channel aware.
    :param enc: encoder function
    :param dec: decoder function
    :return:
    """

    return ColorSpace(_alpha_aware_converter(enc), _alpha_aware_converter(dec))


rgb = _alpha_aware_colorspace(lambda a: a, lambda a: a)
hsv = _alpha_aware_colorspace(rgb2hsv, hsv2rgb)
luv = _alpha_aware_colorspace(rgb2luv, luv2rgb)
hed = _alpha_aware_colorspace(rgb2hed, hed2rgb)
lab = _alpha_aware_colorspace(rgb2lab, lab2rgb)
xyz = _alpha_aware_colorspace(rgb2xyz, xyz2rgb)


def is_scalar(img):
    return len(img.shape) == 2


def is_comp(img):
    return len(img.shape) == 3


def is_3comp(img):
    return len(img.shape) == 3 and img.shape[2] == 3


def is_4comp(img):
    return len(img.shape) == 3 and img.shape[2] == 4


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