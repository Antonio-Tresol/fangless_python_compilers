def test1() -> int:
    return 1


def test2() -> tuple:
    a = [1, 2, 3]
    return 1, 2, 3, a


def test3() -> tuple:
    a = 1
    b = 2
    return a + b * 3, a, b


def test4() -> tuple:
    a = 1
    b = 2

    return a if a > b else b, a, b
