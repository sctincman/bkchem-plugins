
import Pmw



def process_atom_symbol_only( a):
  return a.symbol



def process_atom_symbol_and_hyb_on_C( a):
  if a.symbol == 'C':
    return a.symbol + str( a.degree + a.free_valency - 1)
  else:
    return a.symbol




def process_line( atoms, how="symbol_only"):
  out = []
  for a in atoms:
    out.append( globals()['process_atom_'+how]( a))
  return ' '.join( out)
  




as = [a for a in App.paper.selected if a.object_type == "atom"]
if not len( as) == 1:
  App.log( "You have to have exactly 1 atom selected", message_type="error")
else:
  a = as[0]
  mol = a.molecule
  maxd = mol.mark_vertices_with_distance_from( a)

  dialog = Pmw.TextDialog( App.paper, title=_("Distance matrix"))
  dialog.withdraw()


  for i in range( maxd+1):
    atoms = [a for a in mol.vertices if a.properties_['d'] == i]
    dialog.insert( 'end', process_line( atoms, how="symbol_and_hyb_on_C")+"\n")

  dialog.activate()




