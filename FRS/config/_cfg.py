"""
Defines all classes and common conditions used in FRS Configuration.
"""

from typing import Generic, TypeVar, Callable, Iterable, Type

from util.strutils import TemplateString, TemplateLike, fqn

from funcy.funcs import partial, compose
from funcy.types import isa
from funcy.colls import all, map
from funcy.funcolls import all_fn as join

T = TypeVar('T')
Predicate = Callable[[T], bool]

class ConditionError(RuntimeError):
    def __init__(self, cond: 'Condition', desc):
        super().__init__('%s Not Met: %s' % (fqn(cond), desc))

class Condition(Generic[T]):
    """
    A required property. Wraps a predicate and an error description, offering predicate testing with and without
    failure on given values.
    
    Can generically take anything though can be designed for specific types and combined, functionally, with other
    Condition or predicate functions through function composition. Designed to work with functional approaches to data
    validation.
    """
    
    def __init__(self, condition: Predicate, desc: TemplateLike):
        """
        The condition function must be a predicate that takes a value and returns true or false. The description can be either
        a plain string, a string with formatting variables or a TemplateString. The error description can be formatted to take
        a single named format variable called 'value' which is the value that failed.
        
        :param condition: Predicate function
        :param desc: Error description
        """
        self._cond = condition
        self._desc = TemplateString(desc)
    
    @property
    def error_message(self):
        return self._desc
    
    def test(self, x: T) -> bool:
        """
        Tests if the condition is true for a given value.
        
        :param x: Value to test
        :return: True if meets condition, false otherwise
        """
        return self._cond(x)
    
    def test_with_fail(self, x: T) -> bool:
        """
        Tests if the condition is true for a given value. If the value does not meet the condition (the predicate returns
        false), a RuntimeError is raised with the Condition's error message, formatted with the value.
        
        :param x: Value to test
        :return: True if succeeded, errors otherwise
        :raises RuntimeError: If condition is not met
        """
        if not self._cond(x):
            raise ConditionError(self, self._desc.format(value=x))
        return True
    
    def __call__(self, x: T, *args, **kwargs):
        return self.test_with_fail(x)

class ConfigError(RuntimeError):
    def __init__(self, message: str):
        super().__init__(message)
        

class ConfigValue(Generic[T]):
    """
    A value used for configuration, the beneift of using this over hardcoded values is the ability to set mutability and
    required conditions, which means (assuming an unsuspecting developer does not modify the conditions) config values
    cannot be changed to likely invalid values accidentally with blame (through source control) for invalid values being
    clear.
    """
    def __init__(self, value: T, condition: Callable[[T], bool]=lambda x: True, mutable: bool = False):
        """
        :param value: Value to wrap
        :param condition: A predicate to test the given value on
        :param mutable:
        """
        self._val = value
        self._mutable = mutable
        self._condition = condition
        
        self._test_value()
    
    def _test_value(self):
        try:
            if not self._condition(self.value):
                raise ConfigError("Condition not met: {}.".format(self.value))
        except ConditionError as e:
            raise ConfigError("Condition Not Met") from e
    
    @property
    def value(self) -> T:
        return self._val
    
    @value.setter
    def value(self, x: T) -> None:
        if not self._mutable:
            raise ConfigError("Config Value is Immutable")
        self._val = x
        self._test_value()
    
    def __call__(self, *args, **kwargs):
        return self.value
    
    def __str__(self):
        return "ConfigValue['%s': %s]" % (fqn(self.value), self.value)
    

nonnegative = Condition(lambda x: x >= 0, TemplateString("{value} must be non-negative."))
negative = Condition(lambda x: x < 0, TemplateString("{value} must be negative."))
is_number = Condition(isa(float, int), TemplateString("{value} must be a float or an int."))

def typed_cond(condition: Callable[[T], bool], *types):
    return join(is_type(*types), condition)

def is_type(*types: Iterable[Type]):
    return Condition(isa(*types), "{value} must be of type %s." % list(types))

def any_of(allowed: Iterable[T]):
    return Condition(lambda x: x in allowed, "{value} must be one of %s." % allowed)

def clamped(min: int=0, max: int=1):
    return Condition(lambda x: min <= x <= max, "{value} is not in range [%d, %d]" % (min, max))

def contained_type(*types):
    map_to_types = partial(map, type)
    verify_types = partial(all, lambda x: x in types)
    
    return Condition(compose(verify_types, map_to_types), "All values in {value} must be one of %s." % list(types))
