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
