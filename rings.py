import time


for mol in App.paper.molecules:
  for meth in (mol.get_smallest_independent_cycles_e,):  # mol.get_smallest_independent_cycles):
    #for edges in mol.get_all_cycles_e():
    t1 = time.time()
    rings = meth()
    print "should be", len( mol.edges) - len( mol.vertices) + 1
    print meth, len( rings), [len( ring) for ring in rings]
    print " %.5fs" % (time.time() - t1)

