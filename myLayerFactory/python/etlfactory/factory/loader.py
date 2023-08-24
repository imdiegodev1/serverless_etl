from importlib import import_module
from inspect import getmembers, isabstract, isclass

def loader(factory_name, path = 'factories', abstract = None):
    try:
        factory_module = import_module('.'+factory_name, 'etlfactory.'+path)
    except ImportError:
        factory_module = import_module('.null_factory', path)

    classes = getmembers(factory_module, lambda m: isclass(m) and not isabstract(m))

    for _, _class in classes:
        if issubclass(_class, abstract):
            return _class()
        else:
            raise TypeError("Invalid abstract method")
