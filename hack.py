
import geometry
import misc
import math


rx0, ry0, rx1, ry1 = [200, 200, 300, 260]
x0 = rx0 + (rx1 - rx0) / 3
y0 = (ry0 + ry1) / 2

for i in range( 6400):
  ang = i * math.pi / 3200
  x1 = x0 + 300*math.cos( ang)
  y1 = y0 + 300*math.sin( ang)

  (x, y) = geometry.intersection_of_line_and_rect( (x0, y0, x1, y1), (rx0, ry0, rx1, ry1), round_edges=10.0)
  App.paper.create_line( x, y, x+1, y+1, fill="#000")





