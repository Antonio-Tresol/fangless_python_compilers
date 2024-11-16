def suma(a, b):
    return (a) + (b)


def fibbonacci(n):
    n_1 = 1
    n_2 = 1
    res = 0
    for i in range(2, n):
        res = n_1 + n_2
        n_1 = n_2
        n_2 = res

    return res


def factorial(n):
    if n < 1:
        return 1
    else:
        return n * factorial(n - 1)


f = factorial(5) + 5 // fibbonacci(2)


class Carlitos:
    def __init__(self, b):
        self.a = b
        self.b = 10


class Pepito(Carlitos):
    def __init__(self, b, c):
        self.a = b
        self.b = 10
        self.c = self.b

    def age(self):
        return self.a + self.b + self.c


luis = Pepito(5, 6)
print(luis.age())

a = dict()
a["hola"] = "mundo"


b = {
    "hello": "world",
    "spanish": a,
    "empty": dict(),
    "set": set(),
    1: "1",
    "list": list(),
}


def while_func(n):
    while n > 0:
        print(n)
        n -= 1
        if n == 10:
            break
        if n == 7:
            continue
        if n >= 50000:
            return "Hola"
        elif n > 1000:
            return 1


def ifs(a, b, c, d):
    if a or b:
        print(a)
    elif c:
        if a and b:
            if d:
                print(d)
        elif a:
            if d:
                print(c)
        else:
            print(a)


hi = hola = "hola" + " mundo" + "!"
print(hi)
print(hola)


def hello():
    print("hello")
    mundo()


def mundo():
    print("mundo")
