import typing


def get_type_from_annotation(annotation: typing.Any, /) -> type[typing.Any]:
    t = annotation

    while True:
        if isinstance(t, typing.TypeAliasType):
            t = t.__value__

        origin = typing.get_origin(t)

        if origin is None:
            break

        if origin is typing.Annotated:
            t = typing.get_args(t)[1]
            continue

        t = origin

    return t if isinstance(t, type) else type(t)


__all__ = ("get_type_from_annotation",)
