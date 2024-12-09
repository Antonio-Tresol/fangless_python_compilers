print("count examples:")

# Count occurrences of a value
t = (1, 2, 3, 2, 4, 2)
print(t.count(2))  # Outputs: 3 (2 occurs three times)
print(t.count(3))  # Outputs: 1 (3 occurs once)
print(t.count(5))  # Outputs: 0 (5 does not exist in the tuple)

# Edge case: Empty tuple
t = ()
print(t.count(1))  # Outputs: 0 (no elements to count)

# Count with strings
t = ("a", "b", "a", "c", "a")
print(t.count("a"))  # Outputs: 3
print(t.count("z"))  # Outputs: 0


print("\nindex examples:")

# Find the first index of a value
t = (1, 2, 3, 2, 4, 2)
print(t.index(2))  # Outputs: 1 (first occurrence of 2 is at index 1)
print(t.index(3))  # Outputs: 2 (first occurrence of 3 is at index 2)

# Using start and stop
print(t.index(2, 2))  # Outputs: 3 (search starts at index 2)
print(t.index(4, 4))  # Outputs: 4 (search starts at index 4)

# Index with strings
t = ("a", "b", "a", "c", "a")
print(t.index("a"))  # Outputs: 0 (first occurrence of "a" is at index 0)
print(t.index("c"))  # Outputs: 3
