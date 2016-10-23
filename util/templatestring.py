from typing import Union

import string
import re

TemplateLike = Union[str, 'TemplateString']


_identifier_re = r"(\$\{[^\d\W]\w*\})"

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

    def __init__(self, fmt: str, *args, _format_str: str = None):
        self._original_string = fmt
        self._format_string = _format_str or TemplateString._clean_string(self._original_string)
        self._template = string.Template(self._format_string)

    def format(self, *args, **kwargs) -> str:
        return self._template.safe_substitute(*args, **kwargs)

    def get_format_string(self):
        return self._original_string

    @staticmethod
    def _clean_string(fmt: str) -> str:
        if not isinstance(fmt, str):
            return fmt

        import collections

        def should_substitute(cur_index: int = 0):
            if cur_index + 1 >= len(fmt):
                return False

            cur_char = fmt[cur_index]
            nxt_char = fmt[cur_index + 1]

            return cur_char == '$' and nxt_char != '{'

        match_indices = {m.start(0) for m in re.finditer(_identifier_re, fmt)}

        res = collections.deque()
        for i in range(0, len(fmt)):
            if i not in match_indices and should_substitute(i):
                res.append('$$')
            else:
                res.append(fmt[i])

        return ''.join(res)

    def __eq__(self, other: TemplateLike) -> bool:
        if isinstance(other, str):
            return self._original_string == other
        else:
            return self._original_string == other._original_string

    def __call__(self, *args, **kwargs) -> str:
        return self.format(*args, **kwargs)

    def __getitem__(self, item: int) -> str:
        return self._original_string[item]

    def __str__(self) -> str:
        return 'TemplateStr["{}"]'.format(self._original_string)

    def __bytes__(self) -> bytes:
        return bytes(str(self))

    def __add__(self, other: TemplateLike) -> 'TemplateString':
        if isinstance(other, str):
            return TemplateString(self._original_string + other,
                                  _format_str=self._format_string + TemplateString._clean_string(other))
        else:
            return TemplateString(self._original_string + other._original_string,
                                  _format_str=self._format_string + other._format_string)

    def __radd__(self, other: TemplateLike) -> 'TemplateString':
        if isinstance(other, str):
            return TemplateString(other + self._original_string,
                                  _format_str=TemplateString._clean_string(other) + self._format_string)
        else:
            return TemplateString(other._original_string + self._original_string,
                                  _format_str=other._format_string + self._format_string)
