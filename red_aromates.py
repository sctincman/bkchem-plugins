

app.paper.unselect_all()

for mol in app.paper.molecules:
  mol.mark_aromatic_bonds()
  for b in mol.bonds:
    if b.aromatic:
      b.line_color = "#aa0000"
      b.redraw()


