import time
from singleton_store import Store
from oasa import coords_optimizer


def callback( i, rmsg, maxg):
  if not i % 10:
    Store.log( "%d iterations, RMS grad %f, max grad %f" % (i, rmsg, maxg))
    App.paper.molecules[0].redraw()
    App.update()
    App.update_idletasks()
    #App.mainloop( 10)
    #time.sleep( 0.2)


for mol in App.paper.molecules:
  opt = coords_optimizer.coords_optimizer()
  opt.optimize_coords( mol, bond_length=30, callback=callback)

