import math
from math import sqrt

a = float(input())
b = float(input())

c = math.sqrt(a**2 + b**2)

theta = math.atan(a / b)
theta_degrees = round(math.degrees(theta))

print(f"{theta_degrees}°")
