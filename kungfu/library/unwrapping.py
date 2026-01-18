import inspect
import typing
from functools import wraps

from kungfu.library.error.error import UnwrapError
from kungfu.library.monad.option import Nothing, Option
from kungfu.library.monad.result import Error, Result

type Coroutine[T] = typing.Coroutine[typing.Any, typing.Any, T]
type Function[**P, R] = typing.Callable[P, R]


def cast_error(error: UnwrapError[typing.Any], /) -> Error[typing.Any] | Nothing:
    return error.__error__.cast(Error, lambda _: Nothing())


@typing.overload
def unwrapping[**P, R](func: Function[P, Option[R]], /) -> Function[P, Option[R]]: ...


@typing.overload
def unwrapping[**P, T, Err](func: Function[P, Result[T, Err]], /) -> Function[P, Result[T, Err]]: ...  # type: ignore


@typing.overload
def unwrapping[**P, R](func: Function[P, typing.Awaitable[Option[R]]], /) -> Function[P, Coroutine[Option[R]]]: ...


@typing.overload
def unwrapping[**P, T, Err](func: Function[P, typing.Awaitable[Result[T, Err]]], /) -> Function[P, Coroutine[Result[T, Err]]]: ...  # type: ignore[reportUnknownReturnType]


def unwrapping(func: Function[..., typing.Any], /) -> Function[..., typing.Any]:
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        @typing.no_type_check
        async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            try:
                return await func(*args, **kwargs)
            except UnwrapError as e:
                return cast_error(e)
    else:

        @wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            try:
                return func(*args, **kwargs)
            except UnwrapError as e:
                return cast_error(e)

    return typing.cast("Function[..., typing.Any]", wrapper)


__all__ = ("unwrapping",)
