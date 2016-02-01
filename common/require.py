import os
import sys
import imp
import contextlib
import threading


lock = threading.Lock()


def as_module(file_path, name):
    """
    Requires an arbitrary file. It imports it and assigns it a name.

    It will be a useful tool in our programs requiring somehow a Python plugin.
    :param file_path:
    :param as_module:
    :return:
    """

    with lock:
        with open(file_path, 'U') as module_file:
            prev = sys.dont_write_bytecode
            sys.dont_write_bytecode = True
            module = imp.load_module(name, module_file, file_path, (".py", 'U', imp.PY_SOURCE))
            sys.dont_write_bytecode = prev
            sys.modules[name] = module
            return module





