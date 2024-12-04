# conjugate
print("\nconjugate examples:")
print((5.5).conjugate())  # Outputs: 5.5 (conjugate of a real number is itself)
print((-2.3).conjugate())  # Outputs: -2.3

# imag
print("\nimag examples:")
print((5.5).imag())  # Outputs: 0.0 (imaginary part of a float is always 0.0)
print((-3.2).imag())  # Outputs: 0.0

# is_integer
print("\nis_integer examples:")
print((5).is_integer())  # Outputs: True
print((5.5).is_integer())  # Outputs: False (5.5 is not an integer)
print((0).is_integer())  # Outputs: True
print((-3).is_integer())  # Outputs: True

# real
print("\nreal examples:")
print((5.5).real())  # Outputs: 5.5 (real part of a float is itself)
print((-2.3).real())  # Outputs: -2.3
