import collections.abc


class ThunkDict(collections.abc.MutableMapping):
    DICT_LIKE_EXN = TypeError("dictionary must be a dict-like object")

    class __LazyInternal__(object):
        def __getitem__(self, key):
            return self.key()

        def __call__(self, key, item):
            self.key = lambda: item
            return self

    def __init__(self, dictionary=None, *args, **kwargs):
        self.__lazy__wrapper__ = self.__LazyInternal__()
        self.__dictionary__ = None

        if isinstance(dictionary, dict):
            self.__dictionary__ = dictionary
        elif dictionary is None:
            self.__dictionary__ = {}
        else:
            raise self.DICT_LIKE_EXN

        self.__dictionary__.update(*args, **kwargs)

    def get_dict(self):
        return self.__dictionary__

    def set_dict(self, dictionary):
        self.__dictionary__ = dictionary
        return True

    def keys(self):
        return self.__dictionary__.keys()

    def items(self):
        return self.__dictionary__.items()

    def __getitem__(self, key):
        obj = self.__dictionary__[key]
        self.__dictionary__[key] = obj[key]() if isinstance(
            obj, self.__LazyInternal__) else obj
        return self.__dictionary__[key]

    def __setitem__(self, attr, item):
        self.__dictionary__[attr] = \
            self.__lazy__wrapper__(attr, item) if callable(item) else item
        return True

    def __delitem__(self, key):
        del self.__dictionary__[key]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.__dictionary__)
