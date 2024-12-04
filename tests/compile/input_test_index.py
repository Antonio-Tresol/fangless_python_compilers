print("\nIndexation and Slicing Tests:")

# Indexing with strings
s = "Hello"
print(s[0])        # Expected: 'H'
print(s[-1])       # Expected: 'o'
print(s[1:4])      # Expected: 'ell'
print(s[:3])       # Expected: 'Hel'

# Indexing with lists
lst = [1, 2, 3, 4, 5]
print(lst[0])      # Expected: 1
print(lst[-1])     # Expected: 5
print(lst[1:4])    # Expected: [2, 3, 4]
print(lst[:3])     # Expected: [1, 2, 3]

# Slicing with negative indexes
print(lst[-3:-1])   # Expected: [3, 4]
print(s[-4:-1])     # Expected: 'ell'

# Indexing and slicing with assignment (list modification)
lst[0] = 10
print(lst)          # Expected: [10, 2, 3, 4, 5]

# Empty slicing
print(s[10:15])     # Expected: ''
print(lst[10:15])   # Expected: []
