a = [3, 4, 5, "bro"]
b = a.copy()

while len(a) > 0:
    a.pop()
a = b.copy()
z = 0

while z != 0:
    z += a.pop()
    if z:
        break
else:
    print(z)
