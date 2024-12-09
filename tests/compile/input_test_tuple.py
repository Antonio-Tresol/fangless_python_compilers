print("Testing tuple with lists")
# (1, 2, 3)
print(tuple([1, 2, 3]))
# ('a', 'b', 'c')
print(tuple(['a', 'b', 'c']))
print("")

print("Testing tuple with tuples")
# (1, 2, 3)
print(tuple((1, 2, 3)))
print("")

print("Testing tuple with dicts")
# (1, 2, 3)
print(tuple({1 : "one", 2 : "two", 3 : "three"}))
print("")

print("Testing tuple with strings")
# ('h', 'e', 'l', 'l', 'o')
print(tuple("hello"))
# ('p', 'y', 't', 'h', 'o', 'n')
print(tuple("python"))
print("")

print("Testing tuple with range")
# (0, 1, 2, 3)
print(tuple(range(4)))
# (10, 11, 12)
print(tuple(range(10, 13)))
print("")