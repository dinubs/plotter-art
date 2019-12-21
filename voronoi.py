import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import mlrose

im = Image.open("cat-sm.jpg")
im.load()
im = im.filter(ImageFilter.GaussianBlur(4))
im = im.convert('1')

print("Image Size")
print(im.size)
im.save("cat-tsp.jpg")
a = np.asarray(im)

del im

# draw = ImageDraw.Draw(im)
# draw.ellipse([10, 10, 100, 100], fill=128)
# del draw

# for x in range(width):
# for y in range(height):


points = []
size = 0

it = np.nditer(a, flags=['multi_index'])
while not it.finished:
    if (it[0] == 1):
        points.append(it.multi_index)
        size += 1
    it.iternext()

del a
del it

print(np.asarray(points).nbytes)

# Initialize fitness function object using coords_list
# fitness_coords = mlrose.TravellingSales(coords=points)

problem_fit = mlrose.TSPOpt(length=size, coords=points, maximize=False)

best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)
