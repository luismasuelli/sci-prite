from six import integer_types
from numpy import (
    int_, intp, int8, int16, int32, int64,
    uint8, uint16, uint32, uint64,
    float_, float16, float32, float64
)
from numpy import all as npall


class IN(object):
    """
    Range-check for arrays.
    """

    def __init__(self, minv, maxv, strict_min=False, strict_max=False):
        self.__minv = minv
        self.__maxv = maxv
        self.__strict_min = strict_min
        self.__strict_max = strict_max

    def contains(self, item):
        lower = item > self.__minv if self.__strict_min else item >= self.__minv
        upper = item < self.__maxv if self.__strict_max else item <= self.__maxv
        return lower & upper


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