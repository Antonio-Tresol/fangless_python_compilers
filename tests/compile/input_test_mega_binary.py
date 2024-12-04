print("\nChaotic Arithmetic and Logical Mixes:")
print((5 + 3) * (2 | 1) - (9 // 2) ** (2 & 1))  # 23
print(1 + 2 * 3 == 7 or 8 // 2 == 4)            # True
print((5 < 10) * (4 | 2) + (~3 & 1))            # 6

print("\nBitwise and Logical Chaos:")
print(~(5 & 3 | 2 ^ 1) << 2)                    # -16
print(1 << ((8 & 3) + 2) - (5 ^ 4))             # 2
print(~((10 >> 1) & ~(3 << 1)))                 # -2
print((~42 & 15) | (8 ^ 3))                     # 15
print((10 > 2) & (False or True))               # True

print("\nString and List Manipulations:")
print("Test" * (2 + 3 & 1) + " Chaos")          # Test Chaos
print((["A", "B"] * 2) + ["C"] * (2 & 1))       # ['A', 'B', 'A', 'B']
print("Odd " + "Shift " * (True << 1))          # Odd Shift Shift
print((not 0) * "Truthy")                       # Truthy
print(["Mix"] * ((5 > 2) + (8 | 1)))            # ['Mix', 'Mix', 'Mix', 'Mix', 'Mix', 'Mix', 'Mix', 'Mix', 'Mix', 'Mix']

print("\nAdvanced Logical and Arithmetic Combos:")
print((10 % 4) << (2 * 1) - (3 >> 1))           # 4
print((not (3 > 1)) << 1 | (False + 5))         # 5

print("\nNested Madness:")
print(((5 + 3) << 2) & ((9 // 2) ^ 5))          # 0
print((3 | 2) << (1 * (7 - 3)) ^ (~-1))         # 48
print(((8 % 3) + (4 ** 2)) >> (2 << 1))         # 1
print((not ((7 & 3) ^ 2)) | (10 // 3))          # 3
print(((1 << 3) >> 2) + ((~2) & (3 ^ 5)))       # 6

print("\nType Coercion Shenanigans:")
print(int((True + False) * 1.5) | (2 ^ 1))      # 3
print("Length:" + str(len([1, 2]) << (2 & 3)))  # length:8
print("Magic: " + str(bool(~(5 ^ 3))))          # Magic: True
print((len("abcd") & 3) * ("*" * 3))            # 
print(((4 * 2) > 10) | (not (7 << 2)))          # 0