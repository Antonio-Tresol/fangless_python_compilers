# Testing len with a string
print("Testing len with a string")
# Expected output: 5
print(len("hello"))
# Expected output: 0
print(len(""))
# Expected output: 12
print(len("openai rocks"))
print("")

# Testing len with a list
print("Testing len with a list")
# Expected output: 3
print(len([1, 2, 3]))
# Expected output: 0
print(len([]))
# Expected output: 5
print(len(["apple", "banana", "cherry", "date", "elderberry"]))
print("")

# Testing len with a tuple
print("Testing len with a tuple")
# Expected output: 2
print(len((10, 20)))
# Expected output: 0
print(len(()))
# Expected output: 4
print(len((1, 2, 3, 4)))
print("")

# Testing len with a set
print("Testing len with a set")
# Expected output: 3
print(len({1, 2, 3}))
# Expected output: 0
print(len(set()))
# Expected output: 2
print(len({"apple", "banana"}))
print("")

# Testing len with a dictionary (counts keys)
print("Testing len with a dictionary")
# Expected output: 2
print(len({"key1": "value1", "key2": "value2"}))
# Expected output: 0
print(len({}))
# Expected output: 4
print(len({"a": 1, "b": 2, "c": 3, "d": 4}))
print("")

# Testing len with a range
print("Testing len with a range")
# Expected output: 10
print(len(range(10)))
# Expected output: 0
print(len(range(0)))
# Expected output: 5
print(len(range(5, 10)))
print("")