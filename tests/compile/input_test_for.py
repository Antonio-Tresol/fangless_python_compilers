antonio = [1, 2, 3, 4, 5]
kenneth = ["perrito", "leon", "carro", "delfin", "armadillo"]
for i in antonio:
    print("numero siguiente en la lista:")
    print(i)

for i in range(10):
    print("numero siguiente en range:")
    print(i)

for b in range(10, 20):
    print("numero siguiente en range con inicio:")
    print(b)

for index, value in enumerate(kenneth):
    print("index:")
    print(index)
    print("value:")
    print(value)

listita = [{1, 4}, {2, 5}, {3, 6}]

for i, j in listita:
    print("i:")
    print(i)
    print("j:")
    print(j)

for index, num in enumerate(range(18, 25, 2)):
    print(index)
    print(num)
    if num == 18:
        print("Breaking the habit")
        break
else:
    print("Else")


for index in range(27, 30, 2):
    x = 1
    while x < 3:
        break
    else:
        print("While else")
    print(index)
else:
    print("Else")