# Demonstrating set methods

# add
print("add examples:")
s = {1, 2, 3}
s.add(4)
print(s)  # Outputs: {1, 2, 3, 4}
s.add(2)  # Adding an existing element
print(s)  # Outputs: {1, 2, 3, 4} (no duplicates)
s.add(5)
print(s)  # Outputs: {1, 2, 3, 4, 5}
s.add("hello")
print(s)  # Outputs: {1, 2, 3, 4, 5, 'hello'}

# clear
print("\nclear examples:")
s = {1, 2, 3}
s.clear()
print(s)  # Outputs: set()
s.add(1)
print(s)  # Outputs: {1}
s.clear()
print(s)  # Outputs: set()

# copy
print("\ncopy examples:")
s = {1, 2, 3}
s_copy = s.copy()
print(s_copy)  # Outputs: {1, 2, 3}
s.add(4)
print(s)  # Outputs: {1, 2, 3, 4}
print(s_copy)  # Outputs: {1, 2, 3} (copy is unaffected)
empty_set = set().copy()
print(empty_set)  # Outputs: set()

# difference
print("\ndifference examples:")
s1 = {1, 2, 3}
s2 = {2, 3, 4}
print(s1.difference(s2))  # Outputs: {1}
print(s2.difference(s1))  # Outputs: {4}
print(s1.difference(set()))  # Outputs: {1, 2, 3}
print(set().difference(s2))  # Outputs: set()

# discard
print("\ndiscard examples:")
s = {1, 2, 3}
s.discard(2)
print(s)  # Outputs: {1, 3}
s.discard(4)  # No error if element not found
print(s)  # Outputs: {1, 3}
s.discard(1)
print(s)  # Outputs: {3}
s.discard(3)
print(s)  # Outputs: set()

# intersection
print("\nintersection examples:")
s1 = {1, 2, 3}
s2 = {2, 3, 4}
print(s1.intersection(s2))  # Outputs: {2, 3}
print(s2.intersection(s1))  # Outputs: {2, 3}
print(s1.intersection(set()))  # Outputs: set()
print(set().intersection(s2))  # Outputs: set()

# isdisjoint
print("\nisdisjoint examples:")
print({1, 2, 3}.isdisjoint({4, 5}))  # Outputs: True
print({1, 2, 3}.isdisjoint({3, 4}))  # Outputs: False
print(set().isdisjoint({1}))  # Outputs: True
print({1}.isdisjoint(set()))  # Outputs: True

# issubset
print("\nissubset examples:")
print({1, 2}.issubset({1, 2, 3}))  # Outputs: True
print({1, 4}.issubset({1, 2, 3}))  # Outputs: False
print(set().issubset({1}))  # Outputs: True
print({1}.issubset(set()))  # Outputs: False

# issuperset
print("\nissuperset examples:")
print({1, 2, 3}.issuperset({1, 2}))  # Outputs: True
print({1, 2}.issuperset({1, 4}))  # Outputs: False
print(set().issuperset(set()))  # Outputs: True
print({1}.issuperset(set()))  # Outputs: True

# pop
print("\npop examples:")
s = {1, 2, 3}
print(s.pop())  # Outputs: an arbitrary element, e.g., 1
print(s)  # Remaining elements, e.g., {2, 3}
s.pop()
print(s)  # Outputs: {remaining element}
s.pop()
print(s)  # Outputs: set()

# remove
print("\nremove examples:")
s = {1, 2, 3}
s.remove(2)
print(s)  # Outputs: {1, 3}
s.remove(1)
print(s)  # Outputs: {3}
s.remove(3)
print(s)  # Outputs: set()

# symmetric_difference
print("\nsymmetric_difference examples:")
s1 = {1, 2, 3}
s2 = {2, 3, 4}
print(s1.symmetric_difference(s2))  # Outputs: {1, 4}
print(s2.symmetric_difference(s1))  # Outputs: {1, 4}
print(s1.symmetric_difference(set()))  # Outputs: {1, 2, 3}
print(set().symmetric_difference(s2))  # Outputs: {2, 3, 4}

# union
print("\nunion examples:")
s1 = {1, 2}
s2 = {3, 4}
print(s1.union(s2))  # Outputs: {1, 2, 3, 4}
print(s2.union(s1))  # Outputs: {1, 2, 3, 4}
print(s1.union(set()))  # Outputs: {1, 2}
print(set().union(s2))  # Outputs: {3, 4}

# update
print("\nupdate examples:")
s = {1, 2}
s.update({3, 4})
print(s)  # Outputs: {1, 2, 3, 4}
s.update({2, 5})
print(s)  # Outputs: {1, 2, 3, 4, 5}
s.update(set())
print(s)  # Outputs: {1, 2, 3, 4, 5}
s.update({6})
print(s)  # Outputs: {1, 2, 3, 4, 5, 6}
