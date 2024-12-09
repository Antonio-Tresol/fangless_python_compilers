antonio = [1, 2, 3, 4, 5]
print("Test simple for")
for i in antonio:
    print(i)
print("")


print("Test for with range start")
for i in range(10):
    print(i)
print("")


print("Test for with range start and end")
for b in range(10, 20):
    print(b)
print("")


kenneth = ["perrito", "leon", "carro", "delfin", "armadillo"]
print("Test for with enumerate")
for index, value in enumerate(kenneth):
    print("index: " + index + " : " + value)
print("")


listita = [{1, 4}, {2, 5}, {3, 6}]
print("Test for with pairs")
for i, j in listita:
    print("i: " + i + ", j: " + j)
print("")


print("Test for enumerate and range with start, end and step")
for index, num in enumerate(range(18, 25, 2)):
    print("index: " + index + ", num: " + num)
    if num == 18:
        print("Breaking")
        break
else:
    print("Else")
print("")


print("Test for else")
for index in range(27, 30, 2):
    x = 1
    for x in range(2, 4):
        print("inner x: " + x)
        if x == 3:
            break
    else:
        print("Inner else")
    print("outer index: " + index)
else:
    print("Else")
print("")