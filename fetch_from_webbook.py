


from urllib import urlopen
import re
import oasa_bridge

molfile_link = re.compile( '(<a href=")(.*)(">2d Mol file</a>)')
cas_re = re.compile('(<strong>CAS Registry Number:</strong>)(.*)(</li>)')

def get_mol_from_web_molfile( name):
  url = "http://webbook.nist.gov/cgi/cbook.cgi?Name=%s&Units=SI" % ("+".join( name.split()))
  try:
    stream = urlopen( url)
  except IOError:
    print "not found"
    return None
  cas = ''
  for line in stream.readlines():
    casm = cas_re.search( line)
    if casm:
      cas = casm.group(2)
    m = molfile_link.search( line)
    if m:
      print m.group( 2)
      molfile = urlopen( "http://webbook.nist.gov" + m.group( 2))
      stream.close()
      ret = molfile.read()
      molfile.close()
      return ret, cas
  return None



## ask for the name to fetch

import Pmw

dial = Pmw.PromptDialog( app.paper,
                         title=_('Name'),
                         label_text=_('Give the name of a molecule to fetch:'),
                         entryfield_labelpos = 'n',
                         buttons=(_('OK'),_('Cancel')))
res = dial.activate()
if res == _('OK'):
  name = dial.get()

  # fetch the molfile

  import StringIO

  molcas = get_mol_from_web_molfile( name)
  if molcas:
    mol, cas = molcas
    mol = StringIO.StringIO( mol)
    molec = oasa_bridge.read_molfile( mol, app.paper)
    mol.close()
    app.paper.stack.append( molec)
    molec.draw()
    if cas:
      t = app.paper.new_text( 280, 300, text="CAS: "+cas.strip())
      t.draw()
    app.paper.add_bindings()
    app.paper.start_new_undo_record()
  else:
    app.update_status( "Sorry, molecule with name %s was not found" % name)

