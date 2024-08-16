import math
import matplotlib.pyplot as plt

l1 = 100
l2 = 100
rm = 150

def get_angle(l1, l2, rm) -> float:
    return math.acos((l2**2+rm**2-l1**2)/(2*rm*l2))*180/math.pi

x = list(range(1, 199, 1))
y = [get_angle(l1, l2, rmi) for rmi in x]

plt.plot(x, y)
plt.xlabel("r_m in [mm]")
plt.ylabel("phi_0 in [deg]")
plt.show()