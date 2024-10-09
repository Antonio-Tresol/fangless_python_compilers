def func(
    antonio,
    kenneth,
    joseph,
    brandon,
    luis,
):
    return antonio + kenneth * (luis / brandon)


def func_basada(antonio: int, kenneth: int = 3, joseph = 3):
    result = 3
    if antonio == 3:
        return 10
    elif kenneth is not None:
        return kenneth
    return joseph, result


def func_mas_basada(antonio: int, kenneth: dict, joseph: tuple[int, int]):
    result = 3
    if antonio == 3:
        return 10, result
    elif kenneth is not None:
        return kenneth
    return joseph


def func_mas_mas_basada(
    antonio: int,
    kenneth: dict,
    joseph: tuple[int, int],
) -> int | dict | tuple[int, int]:
    result = 3
    if antonio == 3:
        result = 10
    elif kenneth is not None:
        return kenneth
    else:
        while joseph != joseph:
            result = joseph
    return result

a = 3
b = 4
c = "string"
d = {'key': 'value'}

print(func(a, b, c, d, 5))
print(func(1, 2, 3, 4, 5))

print(func_basada(a, b, c))
print(func_basada(3, None, "test"))

print(func_mas_basada(a, d, (a, b)))
print(func_mas_basada(3, {'a': 1}, (1, 2)))

print(func_mas_mas_basada(a, d, (a, b)))
print(func_mas_mas_basada(3, {'a': 3}, (1, 2)))