import typing
from reprlib import recursive_repr

from typing_extensions import type_repr

from kungfu.library.monad.result import Error, Ok, Result
from kungfu.utilities.annotations import get_type_from_annotation
from kungfu.utilities.runtime_generic import RuntimeGeneric

AnyOk: typing.TypeAlias = Ok[typing.Any]

HEAD: typing.Final = typing.NewType("HEAD", type)


class Sum[*Ts](RuntimeGeneric):
    _value: typing.Any

    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    def __init__(self, value: typing.Any, /) -> None:
        self._value = value

    @recursive_repr()
    def __repr__(self) -> str:
        args = self.get_args()
        return "Sum{}({!r})".format(
            "[{}]".format(", ".join(type_repr(arg) for arg in args))
            if args
            else "",
            self._value,
        )

    def __getitem__[T](self, __t: type[T]) -> Result[T, str]:
        return self.only(__t)

    @property
    def v(self) -> typing.Any:
        """Junction; intersection of Sum types."""

        return self._value

    def get_args(self) -> tuple[typing.Any, ...]:
        """>>> Sum[str, int].get_args()
        >>> (str, int)
        >>> Sum[str, int]("Hello!").get_args()
        >>> (str, int)
        """
        return self.__args__

    def only(self, t: typing.Any = HEAD) -> Result[typing.Any, str]:
        """Sets `Sum` to single type. By default this type is generic leading type.
        ```python
        v = Sum[str, int]("Hello")
        v.only() # Ok('Hello')
        v.only(str) # Ok('Hello')
        v.only(int) # Error("Sum[str, int]('Hello') cannot be set only to type `int`.")
        v.only(list) # Error("Sum[str, int]('Hello') cannot be set only to type `list`.")
        ```
        """

        if t is HEAD:
            t = self.get_args()[0]

        if not isinstance(self._value, get_type_from_annotation(t)):
            return Error(f"`{repr(self)}` cannot be set only to type `{type_repr(t)}`.")

        return AnyOk(self._value)

    def detach(self) -> typing.Any:
        """Detaches head type. To make this customizable Python must implement intersection typing.
        ```python
        v = Sum[str, int]

        v("Hello").detach() #> Error("`Sum[str, int]('Hello')` is of type `str`. Thus, head cannot be detached")

        v(1).detach() #> Ok(Sum[int](1))
        ```
        """

        args = self.get_args()
        if len(args) < 2:
            return Error(f"Cannot detach head from Sum[{', '.join(type_repr(arg) for arg in args)}]: at least two args required.")

        head, *tail = (get_type_from_annotation(arg) for arg in args)
        if isinstance(self._value, head) and not isinstance(self._value, tuple(tail)):
            return Error(f"`{repr(self)}` is of type `{type_repr(args[0])}`. Thus, head cannot be detached.")

        sum_alias = Sum[*args[1:]]  # type: ignore
        return Ok[sum_alias](sum_alias(self._value))  # type: ignore


__all__ = ("Sum",)
