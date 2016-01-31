import collections
from functools import wraps
import numpy
from colormap.expressions import mask

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

    return ColorSpace(encode, decode)


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

    # Other calls are simply proxied.
    def __init__(self, np_image):
        self.np_image = np_image

    def __setattr__(self, key, value):
        if key == 'np_image':
            return super(ColorSpaceWrapper, self).__setattr__(key, value)
        return setattr(self.np_image, key, value)

    def __getattr__(self, item):
        if item == 'np_image':
            return super(ColorSpaceWrapper, self).__getattribute__(item)
        return getattr(self.np_image, item)

    def __getitem__(self, item):
        return self.np_image.__getitem__(item)

    def __setitem__(self, key, value):
        self.np_image.__setitem__(key, value)

    # TODO proxy magic methods.


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
            return mask(self.np_image[:, :, idxes[0]], value)
    else:
        def method(self, *values):
            return mask(self.np_image[:, :, idxes], values)
    return method


class RGB(ColorSpaceWrapper):
    """
    RGB (perhaps with Alpha) color space.
    """

    r, g, b, alpha = band_properties(4)
    r_is, g_is, b_is = mask_bands(0), mask_bands(1), mask_bands(2)
    rg_is, rb_is, gb_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    rgb = mask_bands(0, 1, 2)
    rgba = mask_bands(0, 1, 2, 3)


class HSV(ColorSpaceWrapper):
    """
    HSV (perhaps with Alpha) color space.
    """

    h, s, v, alpha = band_properties(4)
    h_is, s_is, v_is = mask_bands(0), mask_bands(1), mask_bands(2)
    hs_is, hv_is, sv_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    hsv = mask_bands(0, 1, 2)
    hsva = mask_bands(0, 1, 2, 3)


class LUV(ColorSpaceWrapper):
    """
    LUV (perhaps with Alpha) color space.
    """

    l, u, v, alpha = band_properties(4)
    l_is, u_is, v_is = mask_bands(0), mask_bands(1), mask_bands(2)
    lu_is, lv_is, uv_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    luv = mask_bands(0, 1, 2)
    luva = mask_bands(0, 1, 2, 3)


class HED(ColorSpaceWrapper):
    """
    HED (perhaps with Alpha) color space.
    """

    h, e, d, alpha = band_properties(4)
    h_is, e_is, d_is = mask_bands(0), mask_bands(1), mask_bands(2)
    he_is, hd_is, ed_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    hed = mask_bands(0, 1, 2)
    heda = mask_bands(0, 1, 2, 3)


class LAB(ColorSpaceWrapper):
    """
    LAB (perhaps with Alpha) color space.
    """

    l, a, b, alpha = band_properties(4)
    l_is, a_is, b_is = mask_bands(0), mask_bands(1), mask_bands(2)
    la_is, lb_is, ab_is = mask_bands(0, 1), mask_bands(0, 2), mask_bands(1, 2)
    lab = mask_bands(0, 1, 2)
    laba = mask_bands(0, 1, 2, 3)


class XYZ(ColorSpaceWrapper):
    """
    XYZ (perhaps with alpha) color space.
    """

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