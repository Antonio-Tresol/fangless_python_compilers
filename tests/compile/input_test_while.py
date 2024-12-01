a = 5
print("este es el valor de a antes del while:")
print(a)
b = a > 0
print(b)
while a > False:
    a = a - 1
    print("este es el valor de a:")
    print(a)
    if a > 1:
        print("--El valor de a es mayor que 1--")
