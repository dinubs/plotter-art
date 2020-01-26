class QuadTree:
  def __init__(self, x, y, w, h, capacity, small_definition):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.capacity = capacity
    self.small_definition = small_definition
    self.divided = False
    self.rendered = False # This is solely for the renderer, not necessary for normal QuadTree
    self.points = []

  def size(self):
    return (self.w, self.h)

  def split(self):
    splitW = self.w / 2
    splitH = self.h / 2
    self.northwest = QuadTree(self.x         , self.y         , splitW, splitH, self.capacity, self.small_definition)
    self.northeast = QuadTree(self.x + splitW, self.y         , splitW, splitH, self.capacity, self.small_definition)
    self.southwest = QuadTree(self.x         , self.y + splitH, splitW, splitH, self.capacity, self.small_definition)
    self.southeast = QuadTree(self.x + splitW, self.y + splitH, splitW, splitH, self.capacity, self.small_definition)
    self.divided = True

  def contains(self, x, y):
    return x >= self.x and x < self.x + self.w and y >= self.y and y < self.y + self.h

  def small(self):
    return self.w < self.small_definition and self.h < self.small_definition

  def insert(self, x, y):
    if not self.contains(x, y):
      return False

    if len(self.points) < self.capacity and not self.divided:
      self.points.append((x, y))
      return True

    if not self.divided:
      self.split()

    return self.northwest.insert(x, y) or self.northeast.insert(x, y) or self.southwest.insert(x, y) or self.southeast.insert(x, y)

  def center_point(self):
    return (round(self.x + (self.w / 2)), round(self.y + (self.h / 2)))

  def corners(self):
    return ((self.x, self.y), (self.x + self.w, self.y), (self.x + self.w, self.y + self.h), (self.x, self.y + self.h))

  def middle_edges(self):
    return (
      (round(self.x + (self.w / 2)), self.y),
      (self.x + self.w, round(self.y + (self.h / 2))),
      (round(self.x + (self.w / 2)), self.y + self.h),
      (self.x, round(self.y + (self.h / 2)))
    )

  def cells(self):
    if self.divided:
      cell_list = []
      child_cells = [self.northwest.cells(), self.northeast.cells(), self.southwest.cells(), self.southeast.cells()]
      for child_cell_list in child_cells:
        if child_cell_list:
          cell_list.extend(child_cell_list)
      return cell_list
    elif self.small():
      return [self]
    else:
      return False

  def draw(self, pDraw):
    startPoint = (self.x, self.y)
    endPoint = (self.x + self.w, self.y + self.h)

    if self.divided:
      self.northwest.draw(pDraw)
      self.northeast.draw(pDraw)
      self.southwest.draw(pDraw)
      self.southeast.draw(pDraw)
    elif self.small():
      pDraw.rectangle((startPoint, endPoint), outline="black", width=1)
