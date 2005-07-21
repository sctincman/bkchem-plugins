from singleton_store import Store
import os
import logger
import time
import tkFileDialog
import FileDialog

def process_directory( directory):
  files = 0
  for filename in os.listdir( directory):
    f = os.path.join( directory, filename)
    if os.path.isfile( f) and os.path.splitext( f)[1] in (".svg",".cdml"):
      print f
      files += 1
      App.in_batch_mode = True
      p = App.add_new_paper( name=f)
      App._load_CDML_file( f, draw=False)
      found = False
      for mol in App.paper.molecules:
        gen = mol.select_matching_substructures( fragment)
        try:
          gen.next()
        except:
          pass
        else:
          found = True
          break
      if not found:
        App.close_current_paper()
      else:
        App.in_batch_mode = False
        [o.draw() for o in App.paper.stack]
        App.paper.set_bindings()
        App.paper.add_bindings()

  App.in_batch_mode = False
  return files



t = time.time()
selected_mols = [o for o in App.paper.selected_to_unique_top_levels()[0] if o.object_type == 'molecule']


if len( selected_mols) > 1:
  Store.log( "Select only one molecule", message_type="error")

elif len( selected_mols) == 0:
  Store.log( "Select a molecule you want to use as the fragment for search", message_type="error")

else:
  # we may proceed
  Store.logger.handling = logger.batch_mode
  
  fragment = selected_mols[0]

  directory = tkFileDialog.askdirectory( parent=App,
                                         initialdir=App.save_dir or "./")

  if directory:
    files = process_directory( directory)

    t = time.time() - t
    print "%d files, %.2fs, %.2fms per file" % (files, t, 1000*(t/files))

