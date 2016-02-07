from six import integer_types
from numpy import (
    bincount,
    int_, intp, int8, int16, int32, int64,
    uint8, uint16, uint32, uint64,
    float_, float16, float32, float64
)
from numpy import all as npall
from .types import IN


UINT_TYPES = (uint8, uint16, uint32, uint64)


def _valid_int(value):
    """
    Tells whether the value is a valid real number.
    :param value:
    :return:
    """
    return isinstance(value, integer_types + UINT_TYPES)

def rgb_normalize(arr):
    """
    Will normalize a uint8 image to a 0..1-valued image.
      Note that alpha channel will also be affected.
    :param arr:
    :return:
    """

    if arr.dtype == uint8:
        return arr / 255.0
    return arr


def rgb_denormalize(arr):
    """
    Will denormalize a float64 image to a 0..255-valued image.
      Note that alpha channel will also be affected.
    :param arr:
    :return:
    """

    if arr.dtype in (float32, float64):
        return arr * 255.0
    return arr


def dhist(arr, bins=256, excludes_rbound=False, ndtype=uint8, distribution=False):
    """
    Computes a discrete histogram over an array. Since arrays are [0..1] or [0..1) -the user
      must tell that using excludes_rbound=False or True- the bins value will tell how will
      we multiply each member.
    :param arr: The input array.
    :param bins: A > 0 value to scale the bins.
    :param excludes_rbound: The user must tell if the values in the array are lower than 1 or
      include the value 1. If they include it, we must decrement bins.
    :param ndtype: A valid integer type for the values.
    :param distribution: Determines whether the frequencies should be divided by the total amount
      in the result.
    :return: The resulting array.
    """

    # Ensure bins is positive integer
    if bins < 1:
        raise ValueError('bins must be > 0')
    if not _valid_int(bins):
        raise TypeError('bins must be uint8, uint16, uint32, or uint64, or standard Python integer type')
    if not ndtype in UINT_TYPES:
        raise ValueError('ndtype must be uint8, uint16, uint32, or uint64')
    # Flatten the array
    arr = arr.ravel()
    size = arr.size
    # Adjust the bins.
    if not excludes_rbound:
        bins -= 1
    # Calculate the bins.
    result = bincount((arr * bins).astype(ndtype))
    # Normalize the result
    if distribution:
        result /= size
    return result