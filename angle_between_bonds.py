
import geometry
import math

bs = [b for b in App.paper.selected if b.object_type == "bond"]
if not len( bs) == 2:
  App.log( "You have to have 2 bonds selected", message_type="hint")
else:
  angs = [geometry.clockwise_angle_from_east( b.atom1.x-b.atom2.x, b.atom1.y-b.atom2.y) for b in bs]
  a1, a2 = angs
  ret = a1 > a2 and (a1-a2) or (a2-a1)
  App.log( str( 180*ret/math.pi))



