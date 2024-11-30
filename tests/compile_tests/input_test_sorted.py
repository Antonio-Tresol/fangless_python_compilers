# Testing sorted with a list of integers
print("Testing sorted with a list of integers")
# Expected output: [1, 2, 3, 4, 5]
print(sorted([5, 3, 1, 4, 2]))
# Expected output: [-10, 0, 5, 10]
print(sorted([10, -10, 0, 5]))
# Expected output: [] (empty list remains empty)
print(sorted([]))
print("")

# Testing sorted with a list of strings
print("Testing sorted with a list of strings")
# Expected output: ['apple', 'banana', 'cherry']
print(sorted(['banana', 'cherry', 'apple']))
# Expected output: ['A', 'B', 'a', 'b'] (case-sensitive sorting)
print(sorted(['b', 'A', 'B', 'a']))
print("")

# Testing sorted with a list of tuples
print("Testing sorted with a list of tuples")
# Expected output: [(1, 'a'), (2, 'b'), (3, 'c')]
print(sorted([(2, 'b'), (1, 'a'), (3, 'c')]))
# Expected output: [('apple', 2), ('banana', 1), ('cherry', 3)]
print(sorted([('cherry', 3), ('banana', 1), ('apple', 2)]))
print("")

# Testing sorted with strings
print("Testing sorted with strings")
# Expected output: abcdefghijklmnopqrstuvwxyz
print(sorted('slvnukdozefhxigqpywmjcbrta'))
# Expected output: zyxwvutsrqponmlkjihgfedcba
print(sorted('abcdefghijklmnopqrstuvwxyz', True))
print("")

# Testing sorted with reverse True
print("Testing sorted with reverse True")
# Expected output: [5, 4, 3, 2, 1]
print(sorted([1, 2, 3, 4, 5], True))
# Expected output: ['z', 'y', 'x']
print(sorted(['x', 'y', 'z'], True))
print("")

# Testing sorted with a set
print("Testing sorted with a set")
# Expected output: [1, 2, 3]
print(sorted({3, 1, 2}))
# Expected output: ['apple', 'banana', 'cherry']
print(sorted({'cherry', 'banana', 'apple'}))
print("")

# Testing sorted with a dictionary (sorting by keys)
print("Testing sorted with a dictionary (sorting by keys)")
# Expected output: ['a', 'b', 'c']
print(sorted({'b': 2, 'a': 1, 'c': 3}))
# Expected output: [1, 2, 3]
print(sorted({3: 'three', 1: 'one', 2: 'two'}))
print("")

# Testing sorted with a range object
print("Testing sorted with a range object")
# Expected output: [1, 2, 3, 4, 5]
print(sorted(range(5, 0, -1)))
# Expected output: [-3, -2, -1, 0, 1, 2]
print(sorted(range(-3, 3)))
print("")