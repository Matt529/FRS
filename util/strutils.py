from typing import Union, Type, Any
from funcy.funcs import compose

TemplateLike = Union[str, 'TemplateString']


class TemplateString(object):
    """
    Storing a formattable string for later use, can be called like a function and supports adding TemplateStrings
    together and adding strings and TemplateStrings together. Internally uses str.format.

    TemplateString("ab{}c")("foo") -> "abfooc"
    TemplateString("ab{}c").format("foo") -> "abfooc"
    TemplateString("foo{}baz") + TemplateString("Sweet {}!") -> TemplateString("foo{}barSweet {}!")
    TemplateString("foo") + "{}baz" -> TemplateString("foo{}baz")
    "foo" + TemplateString("{}baz") -> TemplateString("foo{}baz")

    Does not support identity operations, TemplateStrings are immutable, a new copy is always made.

    """

    def __init__(self, fmt: str, *args):
        if isinstance(fmt, TemplateString):
            self._format_string = fmt._format_string
        else:
            self._format_string = fmt

    def format(self, *args, **kwargs) -> str:
        return self._format_string.format(*args, **kwargs)

    def get_format_string(self):
        return self._format_string

    def __eq__(self, other: TemplateLike) -> bool:
        if isinstance(other, str):
            return self._format_string == other
        else:
            return self._format_string == other._format_string

    def __call__(self, *args, **kwargs) -> str:
        return self.format(*args, **kwargs)

    def __getitem__(self, item: int) -> str:
        return self._format_string[item]

    def __str__(self) -> str:
        return 'TemplateStr["{}"]'.format(self._format_string)

    def __bytes__(self) -> bytes:
        return bytes(str(self))

    def __add__(self, other: TemplateLike) -> 'TemplateString':
        if isinstance(other, str):
            return TemplateString(self._format_string + other)
        else:
            return TemplateString(self._format_string + other._format_string)

    def __radd__(self, other: TemplateLike) -> 'TemplateString':
        if isinstance(other, str):
            return TemplateString(other + self._format_string)
        else:
            return TemplateString(other._format_string + self._format_string)
    
    # Hopefully TemplateStrings can now be used like normal strings
    def __getattr__(self, item):
        fmt_str = self.get_format_string()
        try:
            attr = getattr(fmt_str, item)
        except AttributeError:
            raise AttributeError("Undefined Attribute on %s: %s" % (fqn(self), item))
            
        def check_result(x = None, *args, **kwargs):
            if isinstance(x, str):              # Return type was a string
                return TemplateString(x)
            else:                               # Anything else is just passed through
                return x
        
        if callable(attr):
            # Wrap any callables, the result will be checked to see if the returned value is a string, if so the value
            # will be wrapped in it's own TemplateString. Effectively making all string functions with string return types
            # return TemplateStrings instead.
            #
            # For python this actually DOES include all magic methods by default, so any operations on strings that
            # are not implemented above will be included in this wrapping.
            return compose(check_result, attr)
        else:
            return attr

def fqn(cls: Union[Type[Any], Any]):
    if isinstance(cls, type):
        return cls.__module__ + "." + cls.__name__
    else:
        return cls.__module__ + "." + type(cls).__name__
    
def varnames_from_fmt(fmt: TemplateLike):
    import _string
    if isinstance(fmt, TemplateString):
        fmt = fmt.get_format_string()
    
    return [fname for _, fname, _, _ in _string.formatter_parser(fmt) if fname]
