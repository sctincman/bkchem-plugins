import time
from singleton_store import Store


for mol in App.paper.molecules:
  if len( mol.vertices) == 1 and not mol.vertices[0].show:
    Store.log( "found some orphan atoms")
    App.paper.select( mol.vertices)

