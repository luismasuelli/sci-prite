import collections
from functools import wraps
import numpy
from common.proxy import Proxy
from six import integer_types
from numpy import (
    int_, intp, int8, int16, int32, int64,
    uint8, uint16, uint32, uint64,
    float_, float16, float32, float64
)
from numpy import all as npall
from .types import IN


def _valid_real(value):
    """
    Tells whether the value is a valid real number.
    :param value:
    :return:
    """
    return isinstance(value, integer_types + (float, int_, intp, int8, int16, int32, int64, uint8, uint16, uint32,
                                              uint64, float_, float16, float32, float64))


def mask(array, value):
    """
    Creates a mask from an array against a value, depending on value's nature:

    * Numbers (any number type):

      mask(arr, 1) is the same as arr == 1

    * List or tuples (flat, containing only numbers):

      mask(arr, (1., 1., 1.)) compares each pixel against a color

      If your image has alpha channel, you must compare like:

      mask(arr, (1., 1., 1., 1.))

      Remember to respect the dimensions or numpy will complain.

    * IN (range) instances:

      mask(arr, IN(0.5, 1., false, true)) will make a mask for pixels
        greater than or equal 0.5 and lower than 1.

    :param array:
    :param value:
    :return:
    """

    if _valid_real(value):
        return array == value
    elif isinstance(value, (list, tuple)):
        if not all(_valid_real(v) for v in value):
            raise TypeError("Cannot mask against list or tuples having values other than valid numbers, or being "
                            "multi-dimensional or irregular sequences")
        return npall(array == value, axis=2)
    elif isinstance(value, IN):
        return value.contains(array)
    else:
        raise TypeError("Cannot take a mask from this argument. Only numpy-accepted numeric types, tuples, lists, or "
                        "`IN` instances are accepted")


class ColorSpace(collections.namedtuple('ColorSpace', ['encoder', 'decoder', 'components'])):

    def __getattribute__(self, item):
        """
        Allows us to recover something like rgb.R or rgb.ALPHA
        """

        if item == 'ALPHA':
            return 3
        if len(item) == 1 and 'Z' >= item >= 'A' and item.lower() in self[2]:
            return self[2].index(item.lower())
        return super(ColorSpace, self).__getattribute__(item)


from skimage.color import (
    rgb2hsv, hsv2rgb,
    rgb2luv, luv2rgb,
    rgb2hed, hed2rgb,
    rgb2lab, lab2rgb,
    rgb2xyz, xyz2rgb,
)


def _alpha_aware_converter(func):
    """
    Returns a new function that will apply the original converter but keep the alpha channel if the image is (W, H, 4).
    :param converter:
    :return:
    """

    @wraps(func)
    def _converter(image):
        if is_4comp(image):
            result = func(image[:, :, :3])
            alpha = image[:, :, 3]
            return numpy.dstack((result, alpha))
        else:
            return func(image)
    return _converter


def _alpha_aware_colorspace_wrapper(enc, dec, wrapper_class):
    """
    Creates a ColorSpace whose functions are alpha-channel aware.
    :param enc: encoder function
    :param dec: decoder function
    :param wrapper_class: a wrapper class to use as object.
    :return:
    """

    enc = _alpha_aware_converter(enc)
    dec = _alpha_aware_converter(dec)

    def encode(image):
        # Forth to wrapped
        return wrapper_class(enc(image))

    def decode(wrapper):
        # Back to plain-rgb
        dec(wrapper.np_image)

    return ColorSpace(encode, decode, wrapper_class.COMPONENTS)


def is_scalar(img):
    return len(img.shape) == 2


def is_comp(img):
    return len(img.shape) == 3


def is_3comp(img):
    return len(img.shape) == 3 and img.shape[2] == 3


def is_4comp(img):
    return len(img.shape) == 3 and img.shape[2] == 4


class ColorSpaceWrapper(Proxy):
    """
    This is just a wrapper for an array describing an image.
    Any operation sent to this object, other than the specifically implemented
      in this object (or any subclass) goes directly to the wrapped object.
    """

    # Other calls are simply proxied.
    def __init__(self, np_image):
        self._ = np_image

    def set(self, components, value):
        """
        Sets each value in the component to value. Value may be an iterable so we can operate
          component-wise.
        NOTES: Since this wrapper is masked, data views will have two dimensions instead of three.
          One is for the pixel index, and other is for pixel component.
        """
        self._[:, components] = value
        return self

    def add(self, components, value):
        """
        Increments each value in the component by value. Value may be an iterable so we can operate
          component-wise.
        NOTES: Since this wrapper is masked, data views will have two dimensions instead of three.
          One is for the pixel index, and other is for pixel component.
        """
        self._[:, components] += value
        return self

    def sub(self, components, value):
        """
        Decrements each value in the component by value. Value may be an iterable so we can operate
          component-wise.
        NOTES: Since this wrapper is masked, data views will have two dimensions instead of three.
          One is for the pixel index, and other is for pixel component.
        """
        self._[:, components] -= value
        return self

    def mul(self, components, value):
        """
        Multiplies each value in the component by value. Value may be an iterable so we can operate
          component-wise.
        NOTES: Since this wrapper is masked, data views will have two dimensions instead of three.
          One is for the pixel index, and other is for pixel component.
        """
        self._[:, components] *= value
        return self

    def div(self, components, value):
        """
        Divides each value in the component by value. Value may be an iterable so we can operate
          component-wise.
        NOTES: Since this wrapper is masked, data views will have two dimensions instead of three.
          One is for the pixel index, and other is for pixel component.
        """
        self._[:, components] /= value
        return self

    def clamp(self, components):
        """
        Clamps each value in the selected components to interval 0..1. Both bounds allowed.
        NOTES: Since this wrapper is masked, data views will have two dimensions instead of three.
          One is for the pixel index, and other is for pixel component.
        """
        self._[:, components] = numpy.clip(self._[:, components], 0., 1.)
        return self

    def rotate(self, components):
        """
        Rotates in modulo-1 each value in the selected components to interval 0..1. Excludes value 1, so be wary.
        NOTES: Since this wrapper is masked, data views will have two dimensions instead of three.
          One is for the pixel index, and other is for pixel component.
        """
        self._[:, components] = self._[:, components] % 1
        return self

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


def mask_bands(*idxes):
    """
    Intended to create a method that checks multiple simultaneous bands.
    That kind of check does not return a boolean, but a mask.

    E.g.
      r_is = bands_check(0)
      rgb_is = bands_check(0, 1, 2)
      rgba_is = bands_check(0, 1, 2, 3)

    Notes: if only one index is provided, a 1-arity method is returned and
      the check is scalar. Scalar checks provide scalar values to mask function
      and stuff like IN can be performed. Other scalar checks behave exactly as
      the __eq__ operator.
    """

    if len(idxes) == 1:
        def method(self, value):
            return mask(self[:, :, idxes[0]], value)
    else:
        def method(self, *values):
            return mask(self[:, :, idxes], values)
    return method


class RGB(ColorSpaceWrapper):
    """
    RGB (perhaps with Alpha) color space.
    """

    COMPONENTS = 'rgb'
    r, g, b, alpha = band_properties(4)
    r_is, g_is, b_is = mask_bands(0), mask_bands(1), mask_bands(2)
    rg_is, rb_is, gb_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    rgb = mask_bands(0, 1, 2)
    rgba = mask_bands(0, 1, 2, 3)


class HSV(ColorSpaceWrapper):
    """
    HSV (perhaps with Alpha) color space.
    """

    COMPONENTS = 'hsv'
    h, s, v, alpha = band_properties(4)
    h_is, s_is, v_is = mask_bands(0), mask_bands(1), mask_bands(2)
    hs_is, hv_is, sv_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    hsv = mask_bands(0, 1, 2)
    hsva = mask_bands(0, 1, 2, 3)


class LUV(ColorSpaceWrapper):
    """
    LUV (perhaps with Alpha) color space.
    """

    COMPONENTS = 'luv'
    l, u, v, alpha = band_properties(4)
    l_is, u_is, v_is = mask_bands(0), mask_bands(1), mask_bands(2)
    lu_is, lv_is, uv_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    luv = mask_bands(0, 1, 2)
    luva = mask_bands(0, 1, 2, 3)


class HED(ColorSpaceWrapper):
    """
    HED (perhaps with Alpha) color space.
    """

    COMPONENTS = 'hed'
    h, e, d, alpha = band_properties(4)
    h_is, e_is, d_is = mask_bands(0), mask_bands(1), mask_bands(2)
    he_is, hd_is, ed_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    hed = mask_bands(0, 1, 2)
    heda = mask_bands(0, 1, 2, 3)


class LAB(ColorSpaceWrapper):
    """
    LAB (perhaps with Alpha) color space.
    """

    COMPONENTS = 'lab'
    l, a, b, alpha = band_properties(4)
    l_is, a_is, b_is = mask_bands(0), mask_bands(1), mask_bands(2)
    la_is, lb_is, ab_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    lab = mask_bands(0, 1, 2)
    laba = mask_bands(0, 1, 2, 3)


class XYZ(ColorSpaceWrapper):
    """
    XYZ (perhaps with alpha) color space.
    """

    COMPONENTS = 'xyz'
    x, y, z, alpha = band_properties(4)
    x_is, y_is, z_is = mask_bands(0), mask_bands(1), mask_bands(2)
    xy_is, xz_is, yz_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    xyz = mask_bands(0, 1, 2)
    xyza = mask_bands(0, 1, 2, 3)


rgb = _alpha_aware_colorspace_wrapper(lambda a: a, lambda a: a, RGB)
hsv = _alpha_aware_colorspace_wrapper(rgb2hsv, hsv2rgb, HSV)
luv = _alpha_aware_colorspace_wrapper(rgb2luv, luv2rgb, LUV)
hed = _alpha_aware_colorspace_wrapper(rgb2hed, hed2rgb, HED)
lab = _alpha_aware_colorspace_wrapper(rgb2lab, lab2rgb, LAB)
xyz = _alpha_aware_colorspace_wrapper(rgb2xyz, xyz2rgb, XYZ)