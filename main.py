from Image import Image
import matplotlib.pyplot as plt

im = Image("svg_files/rev.webp")
im.print()
path = im.sort()
print(path)

