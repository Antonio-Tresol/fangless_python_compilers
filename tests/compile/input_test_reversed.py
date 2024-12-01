# Testing reversed with a list
print("Testing reversed with a list")
# Expected output: [5, 4, 3, 2, 1]
print(list(reversed([1, 2, 3, 4, 5])))
# Expected output: ['c', 'b', 'a']
print(list(reversed(['a', 'b', 'c'])))
# Expected output: [] (empty list remains empty)
print(list(reversed([])))
print("")

# Testing reversed with a tuple
print("Testing reversed with a tuple")
# Expected output: (3, 2, 1)
print(tuple(reversed((1, 2, 3))))
# Expected output: ('z', 'y', 'x')
print(tuple(reversed(('x', 'y', 'z'))))
# Expected output: () (empty tuple remains empty)
print(tuple(reversed(())))
print("")

# Testing reversed with a string
print("Testing reversed with a string")
# Expected output: "olleh"
print((reversed("hello")))
# Expected output: "321"
print((reversed("123")))
# Expected output: "" (empty string remains empty)
print((reversed("")))
print("")

# Testing reversed with a range object
print("Testing reversed with a range object")
# Expected output: [9, 8, 7, 6, 5]
print(list(reversed(range(5, 10))))
# Expected output: [4, 3, 2, 1, 0]
print(list(reversed(range(5))))
# Expected output: [] (empty range remains empty)
print(list(reversed(range(0))))
print("")