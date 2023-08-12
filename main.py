from Image import Image
import numpy as np
import matplotlib.pyplot as plt

im = Image("svg_files/rev.webp")
im.print()
path = im.sort()

print(path)

#for point in path:
#    print(point)

# ensures that the x and y values are between 0 and 1
scale = 1000

x = []
y = []

for idx in range(len(path), 0, -1):
    x.append(path[0])

x = np.array([point[0][0] / scale for point in path])
y = np.array([point[0][1] / scale for point in path])

print(x)
print(y)

fig, axs = plt.subplots(1, 1, figsize=(12, 12))
axs.set_xlim(0, 1)
axs.set_ylim(0, 1)
#axs.scatter(x, y, color="red", s=1)
#plt.show()
axs.plot(x, y, color="blue", linewidth=1)
plt.show()
