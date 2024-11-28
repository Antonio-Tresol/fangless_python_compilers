print("Testing frozenset with lists")
# {1, 2, 3}
print(frozenset([1, 2, 3]))
# {'a', 'b', 'c'}
print(frozenset(['a', 'b', 'c']))
print("")

print("Testing frozenset with strings")
# {'e', 'h', 'l', 'o'}
print(frozenset("hello"))
# {'h', 'n', 'o', 'p', 't', 'y'}
print(frozenset("python"))
print("")

print("Testing frozenset with sets")
# {1, 2, 3}
print(frozenset({1, 2, 3}))
print("")


print("Testing empty frozenset")
# {}
print(frozenset())
print("")
