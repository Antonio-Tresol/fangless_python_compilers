def test1() -> int:
    return 1

def test3() -> tuple:
    a = 1
    b = 2
    return a + b * 3, a, b

def test2(b = {"sup", "bro"}) -> tuple:
    a = [1, 2, b]
    return 1, 2, 3, a

def test4(amigo, kenneth, joseph: int = 3) -> tuple:
    a = 1
    b = 2
    print(amigo)
    print(kenneth)
    print(joseph)

    return a if a > b else b, a, b
