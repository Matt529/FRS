from typing import Generic, TypeVar, Any, Callable, Union
from threading import RLock, Lock, Event

import operator
import abc

T = TypeVar('T')


class AtomicityError(Exception):
    pass


class Atomic(abc.ABC, Generic[T]):
    def __init__(self, reentrant: bool = False):
        self._lock = Lock() if not reentrant else RLock()

    @abc.abstractmethod
    def get(self) -> T:
        raise NotImplementedError('Cannot read this value.')

    @abc.abstractmethod
    def set(self, value: T) -> None:
        raise NotImplementedError('Cannot write this value.')


class _AtomicVarView(object):
    def __get__(self, instance: Atomic[T], owner) -> T:
        return instance.get()


class _AtomicVarAccess(object):
    def __set__(self, instance: Atomic[T], value: T) -> T:
        instance.set(value)
        return value


class _AtomicVarHolder(_AtomicVarView, _AtomicVarAccess):
    pass


class AtomicVar(Atomic, Generic[T]):
    def __init__(self, initial_value: T):
        super().__init__()
        self._value = initial_value
        self.value = _AtomicVarHolder()

    def get(self) -> T:
        return self._value

    def set(self, new_value: T) -> None:
        with self._lock:
            self._value = new_value

    def _operate(self, op, *op_args, **op_kwargs) -> T:
        return op(self.get(), *op_args, **op_kwargs)

    def _roperate(self, op, left: T, *right_args, **op_kwargs):
        return op(left, self.get(), *right_args, **op_kwargs)

    def __abs__(self):
        return AtomicVar(self._operate(operator.abs))

    def __add__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        return AtomicVar(self._operate(operator.add, other))

    def __sub__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        return AtomicVar(self._operate(operator.sub, other))

    def __mul__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        return AtomicVar(self._operate(operator.mul, other))

    def __truediv__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        return AtomicVar(self._operate(operator.truediv, other))

    def __floordiv__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        return AtomicVar(self._operate(operator.floordiv, other))

    def __pow__(self, power: Union[T, 'AtomicVar[T]'], modulo: Union[T, 'AtomicVar[T]']=None) -> 'AtomicVar[T]':
        if isinstance(power, AtomicVar):
            power = power.get()

        if modulo is None:
            return AtomicVar(self._operate(operator.pow, power))
        else:
            return AtomicVar(self._operate(pow, power, modulo))

    def __radd__(self, other: T) -> T:
        return self._roperate(operator.add, other)

    def __rsub__(self, other: T) -> T:
        return self._roperate(operator.sub, other)

    def __rmul__(self, other: T) -> T:
        return self._roperate(operator.mul, other)

    def __rtruediv__(self, other: T) -> T:
        return self._roperate(operator.truediv, other)

    def __rfloordiv__(self, other: T) -> T:
        return self._roperate(operator.floordiv, other)

    def __iadd__(self, other: Union[T, 'AtomicVar[T]']) -> None:
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.add, other))

    def __isub__(self, other: Union[T, 'AtomicVar[T]']) -> None:
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.sub, other))

    def __imul__(self, other: Union[T, 'AtomicVar[T]']) -> None:
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.mul, other))

    def __itruediv__(self, other: Union[T, 'AtomicVar[T]']) -> None:
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.truediv, other))

    def __ifloordiv__(self, other: Union[T, 'AtomicVar[T]']) -> None:
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.floordiv, other))


class AtomicCounter(Atomic[int]):

    def __init__(self):
        super().__init__()
        self._counter_lock = self._lock
        self._is_zero = Event()   # type: Event
        self._count = 0
        self.count = _AtomicVarView()

    def get(self) -> int:
        return self._count

    def set(self, value: int) -> int:
        raise AtomicityError()

    def increment(self) -> 'AtomicCounter':
        with self._counter_lock:
            self._count += 1

            if self._is_zero.is_set():
                self._is_zero.clear()
        return self

    def decrement(self) -> 'AtomicCounter':
        with self._counter_lock:
            self._count -= 1

            if self._count == 0 and not self._is_zero.is_set():
                self._is_zero.set()
        return self

    def is_zero(self):
        with self._counter_lock:
            return self._count == 0

    def wait_for_zero(self, timeout: int = None):
        self._is_zero.wait(timeout)

    def __enter__(self):
        self.increment()

    def __exit__(self, *args):
        self.decrement()
