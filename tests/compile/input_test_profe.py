def random_operation(a, b):
    c = a + b
    return c + a * b + 2.6548


def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    elif n == 0:
        return n / 0
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_d(n):
    n_1 = 1
    n_2 = 1

    while n_1 < n:
        new = n_1 + n_2
        n_2 = n_1
        n_1 = new
    return n_1


def iter_example():
    l = [1, 2.5, 3, "hola", 5, "mundo"]
    it = iter(l)
    for i in l:
        print(next(it))
    return True


def map_ex():
    d = {
        "hola": "mundo",
        1: [1, 2, 3, 4, 5],
        "dict": {'adios': ':D'}
    }
    for k in d.keys():
        print(d[k])

    return "hola" + "mundo"


def default_ex(a='hola'):
    return a


def set_ex():
    a = {1, 2, "hola", 4, 5}
    return 2 in a


def tuple_ex():
    a = (5, 6, 'joseph')
    b = (1, 2, 'valverde')
    return a + b


def slices_ex():
    l = [1, 2, 3, 4, 5, 6, 7, 7, 8, 9]
    print(l[-2])
    print(l[1:-2])
    k = l[1:2] + l[-3:-4]
    return k


def string_ex():
    print("profe"[2:4])
    print("profe"[2:4] + "profe"[0:2] + "profe"[-1])

    print(random_operation(5, 6))

print("fibonacci")
print(fibonacci(4))
print("\n\nfibonacci d")
print(fibonacci_d(4))
print("\n\niter")
print(iter_example())
print("\n\nmap")
print(map_ex())
print("\n\ndefault")
print(default_ex())
print("\n\ntuple")
print(tuple_ex())
print("\n\nset")
print(set_ex())
print("\n\nslices")
print(slices_ex())
print("\n\nstring")
string_ex()
