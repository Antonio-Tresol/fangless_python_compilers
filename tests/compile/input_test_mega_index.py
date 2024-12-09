print("\nIndexation and Slicing Tests:")

# Strings
s = "IntriguingTest"
print(s[1:4])       # Expected: 'ntr'
print(s[-8:-4])     # Expected: 'uing'
print(s[:5])        # Expected: 'Intri'
print(s[4:10])      # Expected: 'iguing'
print(s[1:len(s)])  # Expected: 'ntriguingTest'

# Lists
lst = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(lst[2:5])     # Expected: [30, 40, 50]
print(lst[:3])      # Expected: [10, 20, 30]
print(lst[-6:-3])   # Expected: [50, 60, 70]
print(lst[1:9])     # Expected: [20, 30, 40, 50, 60, 70, 80, 90]
print(lst[3:len(lst)])  # Expected: [40, 50, 60, 70, 80, 90, 100]

# Nested slicing
nested_lst = [[1, 2], [3, 4], [5, 6], [7, 8]]
print(nested_lst[1:3])      # Expected: [[3, 4], [5, 6]]
print(nested_lst[-3:-1])    # Expected: [[3, 4], [5, 6]]


# Mixed types in a list
mixed = [100, "string", [10, 20], (5, 6), {"key": "value"}]
print(mixed[1:4])           # Expected: ['string', [10, 20], (5, 6)]
print(mixed[-4:-2])         # Expected: ['string', [10, 20]]

# Out-of-bound slicing (returns empty list or string)
print(lst[20:25])           # Expected: []
print(s[20:25])             # Expected: ''

# Slicing with empty results
print(lst[4:4])             # Expected: []
print(s[3:3])               # Expected: ''

# Combinations of positive and negative indices
print(lst[3:-3])            # Expected: [40, 50, 60, 70]
print(s[-12:7])             # Expected: 'trigu'

# Slicing with booleans (used as indices via int conversion)
bool_lst = [1, 2, 3, 4, 5]
print(bool_lst[True:4])     # Expected: [2, 3, 4] (True -> 1)
print(bool_lst[0:False])    # Expected: [] (False -> 0)

# Accessing single elements with mixed slicing
single_char = "abcdefg"
print(single_char[2:3])     # Expected: 'c'
print(single_char[-2:-1])   # Expected: 'f'
print(lst[-1:len(lst)])     # Expected: [100]

# Reversed ranges yielding empty results
print(s[5:1])               # Expected: ''
print(lst[4:2])             # Expected: []

# Nested slicing and indexing results
nested_complex = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
print(nested_complex[1:2])            # Expected: [[[5, 6], [7, 8]]]
