print("Testing set with lists")
# {1, 2, 3}
print(set([1, 2, 3]))
# {'a', 'b', 'c'}
print(set(['a', 'b', 'c']))
print("")

print("Testing set with strings")
# {'e', 'h', 'l', 'o'}
print(set("hello"))
# {'h', 'n', 'o', 'p', 't', 'y'}
print(set("python"))
print("")

print("Testing set with tuples")
# {1, 2, 3}
print(set((1, 2, 3)))
print("")

print("Testing set with dicts")
# {1, 2, 3}
print(set({1 : "one", 2 : "two", 3 : "three"}))
print("")

print("Testing set with sets")
# {1, "one", 2, "two", 3, "three"}
print(set({1, "one", 2, "two", 3, "three"}))
print("")

print("Testing empty set")
# {}
print(set())
print("")