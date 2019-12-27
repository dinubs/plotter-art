# Polarizer

Polarizer is a python script that transforms an image into a single line scribble that can be consumed by a Polargraph or Plotter machine. It works by taking advantage of dithering and QuadTrees. First we use the built in dithering function from Pillow and then run a basic QuadTree generation on the generated points to come up with groupings.

- https://en.wikipedia.org/wiki/Quadtree
- https://en.wikipedia.org/wiki/Dither

# TODO

- Implement a TSP solver based on the generated quadtrees
- Transform the generated TSP points into a scribble type line where a loop will be put around each cell in the QuadTree
- Convert that generated line into an SVG to be input to the Polargraph

# Usage

The first argument passed in is the image, and the second is the total number of points you want inside each quadtree. You can run the script using the following command

```
$ python3 polarizer.py zebra.jpg 10
```

![Converted image using the Polarizer script](https://github.com/dinubs/plotter-art/raw/master/sample.png)
