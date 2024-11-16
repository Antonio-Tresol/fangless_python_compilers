for i in range(4):
    print((i * i) / i)

a = [3, 4, 5, 6]

for i, b in enumerate(a):
    print(i + b)

b = 5

for i in range(b):
    print(i)
    if b == 5:
        break
else:
    print("broski")
