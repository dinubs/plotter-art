class QuadTree:
  def __init__(self, x, y, w, h, capacity):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.capacity = capacity
    self.divided = False
    self.points = []

  def split(self):
    splitW = self.w / 2
    splitH = self.h / 2
    self.northwest = QuadTree(self.x         , self.y         , splitW, splitH, self.capacity)
    self.northeast = QuadTree(self.x + splitW, self.y         , splitW, splitH, self.capacity)
    self.southwest = QuadTree(self.x         , self.y + splitH, splitW, splitH, self.capacity)
    self.southeast = QuadTree(self.x + splitW, self.y + splitH, splitW, splitH, self.capacity)
    self.divided = True

  def contains(self, x, y):
    return x >= self.x and x < self.x + self.w and y >= self.y and y < self.y + self.h

  def small(self):
    return self.w < 25 and self.h < 25

  def insert(self, x, y):
    if not self.contains(x, y):
      return False

    if len(self.points) < self.capacity and not self.divided:
      self.points.append((x, y))
      return True

    if not self.divided:
      self.split()

    return self.northwest.insert(x, y) or self.northeast.insert(x, y) or self.southwest.insert(x, y) or self.southeast.insert(x, y)

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

