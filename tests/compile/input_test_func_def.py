def bro(number: int) -> int:
    number = number + 1
    number = number + 1
    amigo()
    return number + 1

def amigo():
    print("amigo")

def brocito(string: str, integer: int) -> str:
    string = string * integer
    for charcito in string:
        print(charcito)
    return string

# def brozote(amigos: list) -> list:
#     string = "amigos: "
#     for amigo in amigos:
#         string = string + amigo + ", "
#     return string

def brozote2(amigos: list, integer: int) -> list:
    num = 0
    amigos[0] = "Joe"
    return amigos * integer, integer + 3 + num

# def brozote3(amigos: list, integer: int) -> list:
#     num = 0
#     amigos[0] = "sebas"
#     print(bro(0))

def with_out_return():
    print("Hello")

def with_return():
    print("Hello")
    return "Bye"
def slicing(a:list) -> list:
    return a[0:3]
a = ["sebas", "brandon", "jose"]
number = 3
print(bro(number))
print(brocito("hola", 3))
# asies = brozote(a)
# print(asies)
print(brozote2(a, 3))
# asies2 = brozote3(a, 3)
# print(asies2)
with_out_return()
some = with_return()
print(some)
b = [1, 2, 3, 4, 5]
print(slicing(b))
c = (1, 2, 3, 4, 5)
print(slicing(c))
d = "hola"
print(slicing(d))