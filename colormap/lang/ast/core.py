class TreeNode(object):

    def label(self):
        return self.__class__.__name__

    def items(self):
        raise iter(self)
