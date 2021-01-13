import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import drawSvg as draw
import argparse
from quadtree import QuadTree
import NN
import random
from math import hypot

parser = argparse.ArgumentParser()
parser.add_argument("image", help="set image to polarize")
parser.add_argument("capacity", type=int, help="set cell capacity")
parser.add_argument("small", type=int, help="definition of a small cell")
parser.add_argument("--mode", default="squiggle", choices=["line", "squiggle"], help="polarize in line mode")
parser.add_argument("--debug", action="store_true", help="turn on debug mode")
args = parser.parse_args()

capacity = args.capacity
image = args.image
small = args.small
mode = args.mode
debug = args.debug

if debug:
  print("--- Debug Mode ---")

im = Image.open(image)
width, height = im.size
im.load()
im = im.convert('1')
# im = im.resize((round(width * .1), round(height * .1)))
im.save('dither.jpg')
width, height = im.size

print("------------")
print("Image Size")
print(im.size)
print("Render Mode")
print(mode)
print("------------")
a = np.asarray(im)

qtree = QuadTree(0, 0, width, height, capacity, small)

it = np.nditer(a, flags=['multi_index'])
while not it.finished:
  if (it[0] == 0):
    y, x = it.multi_index
    qtree.insert(x, y)
  it.iternext()

del a
del it

rendered = Image.new('RGBA', im.size, (255,255,255,255))
d = ImageDraw.Draw(rendered)

qtree.draw(d)

small_cells = np.array(qtree.cells())
print
print(len(small_cells))

grouped_cells = {}
points = []
for cell in small_cells:
  grouped_cells[cell.center_point()] = cell
  points.append(cell.center_point())

print("Solving TSP")
lst = NN.tsp(points)

print("Drawing SVG")
d = draw.Drawing(width, height)
start_x, start_y = grouped_cells[lst[0]].center_point()
color = 'black'
for point in lst:
  x, y = cell.center_point()
  w, h = cell.size()
  distance = hypot(x - start_x, y - start_y)

  if debug:
    color = "#%06x" % random.randint(0, 0xFFFFFF)
    print(color)
    print(distance)

  if (distance > 10):
    start_x, start_y = x, y

  p = draw.Path(stroke_width=1, stroke=color, fill='none')
  cell = grouped_cells[point]
  corners = cell.corners
  edges = cell.middle_edges()

  p.M(start_x, start_y)
  if mode == "line":
    p.L(x, y)
  elif mode == "squiggle":
    corners = random.sample(list(cell.corners()), len(cell.corners()))
    for index, corner in enumerate(corners):
      edge = edges[index]
      p.Q(corner[0], corner[1], edge[0], edge[1])

  start_x, start_y = x, y
  d.append(p)

d.saveSvg('rendered.svg')

rendered.show()
