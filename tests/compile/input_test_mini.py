def bro(a=3, b=4) -> int:
    a = a + 1
    a = a + 1
    return a + 1
print(bro())
print(bro(4))
print(bro(4, 5))

def brosote(str_name: str = "abrazo", limit: int =4)-> str:
    str_name = str_name * limit
    return str_name[2:limit]
a= "abrazo abrazo"
print(brosote(a, len(a)))
print(a)
print(brosote())