from typing import Union

import string

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

    def __init__(self, fmt: str):
        self._format_string = fmt
        self._template = string.Template(fmt)

    def format(self, *args, **kwargs) -> str:
        return self._template.safe_substitute(*args, **kwargs)

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
