
import Pmw
import Tkinter
import widgets
import os
import transform
import tempfile


class ActiveDialog( Pmw.Dialog):

  def __init__( self, parent, mol):
    self.mol = mol

    Pmw.Dialog.__init__( self,
                         parent,
                         buttons=(_('Go'),_('Exit')),
                         defaultbutton=_('Go'),
                         title=_('Gamess runner'),
                         command=self.go,
                         master='parent')

    # ui
    self.frame = Tkinter.Frame( self.interior())
    self.frame.pack()
    # handlers
    guessed_inp = os.path.splitext( App.paper._get_full_path())[0] + ".inp"
    self.inp_file = widgets.FileSelectionEntry( self.frame,
                                                prompt =_("Input filename: "),
                                                value = guessed_inp,
                                                filetypes=((_("Gamess input files"), ("*.inp",)),),
                                                type = "save"
                                                )
    self.inp_file.pack()
    
    guessed_out = os.path.splitext( App.paper._get_full_path())[0] + ".out"
    self.out_file = widgets.FileSelectionEntry( self.frame,
                                                prompt =_("Output filename: "),
                                                value = guessed_out,
                                                filetypes=((_("Gamess output files"), ("*.out",)),),
                                                type = "save"
                                                )
    self.out_file.pack()

    self.name = Pmw.EntryField( self.frame,
                                labelpos="w",
                                label_text="Name",
                                value = "",
                                )
    self.name.pack()

    
    # output
    self.text = Pmw.ScrolledText( self.interior())
    self.text.pack( expand=1, fill="both")




  def go( self, res):
    if res == _("Go"):
      inp = self.inp_file.entry.get()
      out = self.out_file.entry.get()

      # save input file
      self.write_input_file()
      self.write( "* input file %s written" % inp)

      # run gamess
      self.write( "* running gamess...")
      dirname, filename = os.path.split( inp)
      os.chdir( dirname)
      ret = os.system( "gamess-single %(inp)s > %(out)s 2>&1" % {'inp': filename,
                                                                 'out': out})
      self.write( "  gamess finished")
      if ret:
        self.write( "! it seems something went wrong :(")

      # convert the output to molfile
      molname = os.path.join( tempfile.gettempdir(), "gamess.mol")
      os.system( "babel -igamout -omol %(out)s %(molname)s" % {'out': out, 'molname': molname})
      print os.stat( "/tmp/gamess.mol").st_size
      self.write( "* molfile converted")

      # import the molfile
      App.add_new_paper()
      plugin = App.plugins[ "Molfile"]
      importer = plugin.importer( App.paper)
      ms = importer.get_molecules( molname)
      #self.paper.create_background()
      for m in ms:
        App.paper.stack.append( m)
        m.draw()
      App.paper.add_bindings()
      App.paper.start_new_undo_record()

      



    else:
      self.deactivate()
  

  def write_input_file( self):
    path = self.inp_file.entry.get()
    inp = file( path, "wt")
    inp.write( """ $CONTRL SCFTYP=RHF RUNTYP=OPTIMIZE COORD=CART $END
 $CONTRL EXETYP=RUN MPLEVL=0 NZVAR=0 $END
 $SYSTEM TIMLIM=1550 MEMORY=5000000 $END
 $BASIS GBASIS=PM3 NGAUSS=6 NDFUNC=0 NPFUNC=0 $END 
 $STATPT NSTEP=250 $END
 $SCF DIRSCF=.TRUE. $END
 $DFT DFTTYP=NONE $END
 $GUESS GUESS=HUCKEL $END
$ZMAT DLC=.T. AUTO=.T. $END
 $DATA
%(name)s
C1
""" % {'name': self.name.get()})

    tr = transform.transform()
    bbox, bl = self.mol.get_geometry()
    tr.set_move( -(bbox[0]+bbox[2])/2, -(bbox[1]+bbox[3])/2)
    tr.set_scaling( 1.35 / bl)
    
    for a in self.mol.atoms:
      x, y = tr.transform_xy( a.x, a.y)
      inp.write( " %(symbol)s    %(ord).1f   %(x)f   %(y)f   %(z)f\n" % {"symbol": a.symbol,
                                                                         "ord": a.symbol_number,
                                                                         "x": x,
                                                                         "y": y,
                                                                         "z": a.z*1.35/bl} )
    inp.write( " $END\n\n")



  def write( self, msg):
    self.text.appendtext( msg+"\n")
    self.text.update()


  def clean( self):
    self.text.clear()
    


### the code itself

ms = [m for m in App.paper.selected_to_unique_top_levels()[0] if m.object_type == "molecule"]

if not len( ms) == 1:
  App.log( "You have to have exactly 1 molecule selected", message_type="error")
else:
  mol = ms[0]

  dialog = ActiveDialog( App.paper, mol)
  dialog.withdraw()


  dialog.activate()



