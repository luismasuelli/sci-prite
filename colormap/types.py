

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
