# Demonstrating list methods

# append
print("append examples:")
lst = [1, 2, 3]
lst.append(4)
print(lst)  # Outputs: [1, 2, 3, 4]
lst.append("hello")
print(lst)  # Outputs: [1, 2, 3, 4, 'hello']
lst.append([5, 6])
print(lst)  # Outputs: [1, 2, 3, 4, 'hello', [5, 6]]

# clear
print("\nclear examples:")
lst = [1, 2, 3]
lst.clear()
print(lst)  # Outputs: []
lst.append(10)
print(lst)  # Outputs: [10]
lst.clear()
print(lst)  # Outputs: []

# copy
print("\ncopy examples:")
lst = [1, 2, 3]
lst_copy = lst.copy()
print(lst_copy)  # Outputs: [1, 2, 3]
lst.append(4)
print(lst)  # Outputs: [1, 2, 3, 4]
print(lst_copy)  # Outputs: [1, 2, 3] (copy is unaffected)
empty_copy = [].copy()
print(empty_copy)  # Outputs: []

# count
print("\ncount examples:")
lst = [1, 2, 2, 3, 3, 3]
print(lst.count(2))  # Outputs: 2
print(lst.count(3))  # Outputs: 3
print(lst.count(4))  # Outputs: 0
print([].count(1))   # Outputs: 0

# extend
print("\nextend examples:")
lst = [1, 2, 3]
lst.extend([4, 5])
print(lst)  # Outputs: [1, 2, 3, 4, 5]
lst.extend((6, 7))
print(lst)  # Outputs: [1, 2, 3, 4, 5, 6, 7]
lst.extend([])
print(lst)  # Outputs: [1, 2, 3, 4, 5, 6, 7]

# index
print("\nindex examples:")
lst = [1, 2, 3, 4, 5]
print(lst.index(3))  # Outputs: 2
print(lst.index(1))  # Outputs: 0

# insert
print("\ninsert examples:")
lst = [1, 2, 3]
lst.insert(1, "hello")
print(lst)  # Outputs: [1, 'hello', 2, 3]
lst.insert(0, "start")
print(lst)  # Outputs: ['start', 1, 'hello', 2, 3]
lst.insert(len(lst), "end")
print(lst)  # Outputs: ['start', 1, 'hello', 2, 3, 'end']

# pop
print("\npop examples:")
lst = [1, 2, 3]
print(lst.pop())  # Outputs: 3
print(lst)  # Outputs: [1, 2]
print(lst.pop(0))  # Outputs: 1
print(lst)  # Outputs: [2]

# remove
print("\nremove examples:")
lst = [1, 2, 3, 2]
lst.remove(2)
print(lst)  # Outputs: [1, 3, 2]
lst.remove(2)
print(lst)  # Outputs: [1, 3]

# reverse
print("\nreverse examples:")
lst = [1, 2, 3, 4]
lst.reverse()
print(lst)  # Outputs: [4, 3, 2, 1]
lst.reverse()
print(lst)  # Outputs: [1, 2, 3, 4]
empty_list = []
empty_list.reverse()
print(empty_list)  # Outputs: []

# sort
print("\nsort examples:")
lst = [3, 1, 4, 1, 5]
lst.sort()
print(lst)  # Outputs: [1, 1, 3, 4, 5]
lst.sort(True)
print(lst)  # Outputs: [5, 4, 3, 1, 1]
words = ["banana", "apple", "cherry"]
words.sort()
print(words)  # Outputs: ['apple', 'banana', 'cherry']