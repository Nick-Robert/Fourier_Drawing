import numpy as np
import matplotlib.pyplot as plt
from svg.path import parse_path
from svg.path.path import Close
from xml.dom import minidom

doc = minidom.parse('C:/Users/nickr/Documents/Programming/Visual_Studio/Fourier_Project/svg_files/rev.svg')
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
doc.unlink()

# define how many points on each path object will be taken
# since each path's .point() method takes a value from 0.0 to 1.0, the number will be 1.0 / N
N = 50

pic_points = []
# print the line draw commands
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        # if not isinstance(e, Close):
        time_num = 0
        while (time_num <= 1.0):
            pic_points.append(e.point(time_num))
            time_num += (1.0/N)
# print(pic_points)
x = [i.real for i in pic_points]
y = [i.imag for i in pic_points]

# initialize the plot
fig, axs = plt.subplots(1, 1, sharex=True, figsize=(12, 12))
fig.suptitle(r'Sampled svg file')
axs.scatter(x, y, color='black', s=1)
plt.show()