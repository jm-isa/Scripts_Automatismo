# -*- coding: utf-8 -*-
import time
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
import rtds.rscadfx


class RTDSModel:
  
  # def __init__( self, casefx ):
  #   return

  def get_connection( self ):
    return rtds.rscadfx.remote_connection()
  
  def init_vars( self, casefx ):
    self.casefx= casefx
    
    # Objects  
    self.flt_bt= casefx.get_object_by_name( "FLT", BUTTON )
    self.flt_duration_sld= casefx.get_object_by_name( "FLTDUR", SLIDER )    

    self.line_length= {
      "LN1": casefx.get_object_by_name( "Length_LN1", SLIDER ),
      "LN3": casefx.get_object_by_name( "Length_LN3", SLIDER ),
      "LN4": casefx.get_object_by_name( "Length_LN4", SLIDER )
    }

    self.resistance= {
      "LN1": casefx.get_object_by_name( "Ron_LN1", SLIDER ),
      "LN2": casefx.get_object_by_name( "Ron_LN2", SLIDER ),
      "LN3": casefx.get_object_by_name( "Ron_LN3", SLIDER ),
      "LN4": casefx.get_object_by_name( "Ron_LN4", SLIDER )
    }

    self.flt_location= casefx.get_object_by_name( 'FLT_LOC', 'dial' )

    self.flt_loc= {
      "LN1": 1,
      "LN2": 2,
      "LN3": 3,
      "LN4": 4    
    } 

    self.flt_tp= {
      "AG": casefx.get_object_by_name( "AG", SWITCH ),
      "BG": casefx.get_object_by_name( "BG", SWITCH ),
      "CG": casefx.get_object_by_name( "CG", SWITCH ),
      "AB": casefx.get_object_by_name( "AB", SWITCH ),
      "BC": casefx.get_object_by_name( "BC", SWITCH ),
      "CA": casefx.get_object_by_name( "CA", SWITCH )
    }

    self.Opn_CBs= {
      "Opn3_C110_bt": casefx.get_object_by_name( "Opn3_C110", BUTTON ),
      "Opn3_C010_bt": casefx.get_object_by_name( "Opn3_C010", BUTTON )
    }
    
    self.Cls_CBs= {
      "Cls3_C110_bt": casefx.get_object_by_name( "Cls3_C110", BUTTON ),
      "Cls3_C010_bt": casefx.get_object_by_name( "Cls3_C010", BUTTON )
    }

    self.Opn_DSs= {
      "Opn_DS_LN2_Bus1_bt": casefx.get_object_by_name( "Opn_DS_LN2_Bus1", BUTTON ),
      "Opn_DS_LN2_Bus2_bt": casefx.get_object_by_name( "Opn_DS_LN2_Bus2", BUTTON )
    }
    
    self.Cls_DSs= {
      "Cls_DS_LN2_Bus1_bt": casefx.get_object_by_name( "Cls_DS_LN2_Bus1", BUTTON ),
      "Cls_DS_LN2_Bus2_bt": casefx.get_object_by_name( "Cls_DS_LN2_Bus2", BUTTON )
    }
      
    # self.plot_ctn= casefx.get_object_by_name( "Fault Bus", PLOT_CONTAINER )
    # self.volts= casefx.get_signal( "Subsystem #1|Node Voltages|S1) N3A" )
  
  
  def push_button( self, element, time_delay= 0.1 ):    
    element.position= 1
    time.sleep( time_delay )
    element.position= 0
    time.sleep( time_delay )


  def checkpoint_sim( self ):
    
    print( "----------CheckPoint!----------" )
  
    self.flt_bt.position= 0
    self.flt_duration_sld.value= 0.1
    self.flt_location.position= 1

    for ln in self.line_length.values(): ln.value= 50
    for res in self.resistance.values(): res.value= 1
    for sw in self.flt_tp.values(): sw.position= 0

    for cb in self.Cls_CBs:
      self.push_button( self.Cls_CBs[ cb ] )

    for ds in self.Cls_DSs:
      self.push_button( self.Cls_DSs[ ds ] )
      
    time.sleep( 1 )


  def fault_res( self, r_falla, pto_falla ):  
    self.resistance[ pto_falla ].value= float( r_falla )      
    print( f"RFalla= { r_falla }" )
      

  def fault_dist( self, dist, caso, pto_falla ):
    
    if caso == 11 or caso == 12:
      self.line_length[ "LN1" ].value= int( dist )
    else:
      self.line_length[ pto_falla ].value= int( dist )
    
    print( f"Fault Distance= { dist }" )


  def fault_dur( self, tf ):    
    self.flt_duration_sld.value= float( tf )    
    print( f"Fault Duration= { tf }" )


  def fault_type( self, tp, value= 1 ):

    if tp == "AG": self.flt_tp[ "AG" ].position= value
    elif tp == "BG": self.flt_tp[ "BG" ].position= value
    elif tp == "CG": self.flt_tp[ "CG" ].position= value
    elif tp == "AB" or tp == "BA": self.flt_tp[ "AB" ].position= value
    elif tp == "BC" or tp == "CB": self.flt_tp[ "BC" ].position= value
    elif tp == "CA" or tp == "AC": self.flt_tp[ "CA" ].position= value
    elif tp == "ABG" or tp == "BAG":
      self.flt_tp[ "AG" ].position, self.flt_tp[ "BG" ].position= value, value
    elif tp == "ACG" or tp == "CAG":
      self.flt_tp[ "AG" ].position, self.flt_tp[ "CG" ].position= value, value
    elif tp == "BCG" or tp == "CBG":
      self.flt_tp[ "BG" ].position, self.flt_tp[ "CG" ].position= value, value
    elif tp == "ABCG":
      self.flt_tp[ "AG" ].position, self.flt_tp[ "BG" ].position, self.flt_tp[ "CG" ].position= value, value, value

    print( f"Fault Type= { tp }" )
    





  
      




