import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from quadtree import QuadTree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("image", help="set image to polarize")
parser.add_argument("capacity", type=int, help="set cell capacity")
args = parser.parse_args()

capacity = args.capacity
image = args.image

im = Image.open(image)
im.load()
im = im.convert('1')

print("Image Size")
print(im.size)
a = np.asarray(im)

width, height = im.size

qtree = QuadTree(0, 0, width, height, capacity)

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

cells = []

def parse_tree(cell):
  if cell.divided:
    parse_tree(cell.northwest)
    parse_tree(cell.northeast)
    parse_tree(cell.southwest)
    parse_tree(cell.southeast)
  elif cell.small():
    cells.append(cell)

parse_tree(qtree)
qtree.draw(d)

print(len(cells))

rendered.show()
