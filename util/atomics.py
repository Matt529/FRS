"""
    Module offering support for Atomic data and utilities. Atomic types intend to have all operations done atomically.
    For example, integer addition is an atomic operation. Nothing else can happen to the involved variables or literals
    until the operation is finished. With AtomicVar for instance, the get/set methods and all supported operators
    are atomic and block off access to that value until the current operation is complete. If the operation was not
    atomic then a set operation is really mutli-instruction and any threads operating in parallel on the same instance
    may modify the object's state before a set operation is complete, meaning the modification is lost.

    The Atomic objects attempt to ensure this in a fairly simple way using python Locks
"""

from typing import Generic, TypeVar, Any, Callable, Union
from threading import RLock, Lock, Event

import operator
import abc

import functools

T = TypeVar('T')


class AtomicityError(Exception):
    pass


class Atomic(abc.ABC, Generic[T]):
    """
    ABC for a class implementing Atomic semantics. The common thread between Atomics is the existence of a Lock in
    Python, since Compare-and-Swap semantics are not really a thing here.
    """
    def __init__(self, reentrant: bool = False):
        self._lock = RLock() if reentrant else Lock()

    @abc.abstractmethod
    def get(self) -> T:
        raise NotImplementedError('Cannot read this value.')

    @abc.abstractmethod
    def set(self, value: T) -> None:
        raise NotImplementedError('Cannot write this value.')


@functools.total_ordering
class AtomicVar(Atomic, Generic[T]):
    """
    Atomic Variable, all operations are considered atomic operations to prevent thread contention.

    The goal is to implement most if not all of the operator methods, but likely many are missing.
    """

    def __init__(self, initial_value: T):
        super().__init__()
        self._value = initial_value

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

    def __iadd__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.add, other))
        return self

    def __isub__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.sub, other))
        return self

    def __imul__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.mul, other))
        return self

    def __itruediv__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.truediv, other))
        return self

    def __ifloordiv__(self, other: Union[T, 'AtomicVar[T]']) -> 'AtomicVar[T]':
        if isinstance(other, AtomicVar):
            other = other.get()
        self.set(self._operate(operator.floordiv, other))
        return self

    def __eq__(self, other: Union[T, 'AtomicVar[T]']) -> bool:
        if isinstance(other, AtomicVar):
            other = other.get()
        return self.get() == other

    def __lt__(self, other: Union[T, 'AtomicVar[T]']) -> bool:
        if isinstance(other, AtomicVar):
            other = other.get()
        return self.get() < other

    def __repr__(self):
        return "AtomicVar[%s]" % self.get()

    def __str__(self):
        return str(self.get())

    value = property(get, set)


class AtomicCounter(Atomic[int]):
    """
    A counter that can be incremented and decremented. The goal is to perform these operations atomically by ensuring
    thread synchronization.

    An instance of this class can also be used in with-statements. On entering the counter is incremented by one and
    one exiting the counter is decremented by one. One use case for this feature is tracking how many threads are
    accessing a particular block of code in the case the threads are not immediately accessible.
    """

    def __init__(self):
        super().__init__()
        self._counter_lock = self._lock

        self._is_zero = Event()   # type: Event
        self._count = 0

    def get(self) -> int:
        """
        Get current counter value
        :return: Current counter value
        """
        return self._count

    def set(self, value: int) -> int:
        """
        Not a valid operation on a counter, raises AtomicityError
        """
        raise AtomicityError()

    def increment(self) -> 'AtomicCounter':
        """
        Atomically increment counter variable. This AtomicCounter is returned for chaining.
        :return: self
        """
        with self._counter_lock:
            self._count += 1

            if self._is_zero.is_set():
                self._is_zero.clear()
        return self

    def decrement(self) -> 'AtomicCounter':
        """
        Atomically decrement counter variable. This AtomicCounter is returned for chaining.
        :return: self
        """
        with self._counter_lock:
            self._count -= 1

            if self._count == 0 and not self._is_zero.is_set():
                self._is_zero.set()
        return self

    def is_zero(self):
        """
        Atomically checks if the current count is 0
        :return: True if count is zero, false otherwise
        """
        with self._counter_lock:
            return self._count == 0

    def wait_for_zero(self, timeout: float = None):
        """
        Wait for the counter to reach zero. If the counter is already zero, this method returns immediately.

        This is managed exclusively through a threading.Event object.

        :param timeout:
            Maximum number of seconds to wait, or None. If None, waits as long as necessary.
        """
        self._is_zero.wait(timeout)

    def __enter__(self):
        self.increment()

    def __exit__(self, *args):
        self.decrement()

    def __str__(self):
        return "AtomicCounter[%s]" % self._count

    def __repr__(self):
        return str(self)

    count = property(get)
