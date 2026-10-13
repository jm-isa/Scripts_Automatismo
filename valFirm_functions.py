# -*- coding: utf-8 -*-
import time
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
import rtds.rscadfx
import pandas as pd


class RTDSModel:
  
  # def __init__( self, casefx ):
  #   return

  def get_connection( self ):
    return rtds.rscadfx.remote_connection()
  
  def init_vars( self, casefx ):
    self.casefx= casefx
    
    # Objects  
    self.flt_bt= casefx.get_object_by_name( "FLT", BUTTON )
    self.flt_Case10_bt= casefx.get_object_by_name( "FLT_Case10", BUTTON )
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

    self.flt10= {
      "flt10_1": casefx.get_object_by_name( "FLT10_1", SLIDER ),
      "flt10_2": casefx.get_object_by_name( "FLT10_2", SLIDER )
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
    
    self.goose_signals= {
      "g__C110_3_TRIP": "Subsystem #1|GTNET|GTNET1|g__C110_3_TRIP",
      "g__PROT_C110_A_Trip": "Subsystem #1|GTNET|GTNET1|g__PROT_C110_A_Trip",
      "g__PROT_C110_B_Trip": "Subsystem #1|GTNET|GTNET1|g__PROT_C110_B_Trip",
      "g__PROT_C110_C_Trip": "Subsystem #1|GTNET|GTNET1|g__PROT_C110_C_Trip",
      "g__C010_3_TRIP": "Subsystem #1|GTNET|GTNET1|g__C010_3_TRIP",
      "g__PROT_C010_A_Trip": "Subsystem #1|GTNET|GTNET1|g__PROT_C010_A_Trip",
      "g__PROT_C010_B_Trip": "Subsystem #1|GTNET|GTNET1|g__PROT_C010_B_Trip",
      "g__PROT_C010_C_Trip": "Subsystem #1|GTNET|GTNET1|g__PROT_C010_C_Trip",
      "g__Pickup_Z1": "Subsystem #1|GTNET|GTNET1|g__Pickup_Z1"
    }    
    
    self.goose_dict= { 
      signal: { "path": path, "object": casefx.get_signal( path )  } 
      for signal, path in self.goose_signals.items() 
    }
    
    self.fltln_signals= {
      "FLTLN1": "Subsystem #1|CTLs|Vars|FLTLN1",
      "FLTLN2": "Subsystem #1|CTLs|Vars|FLTLN2",
      "FLTLN3": "Subsystem #1|CTLs|Vars|FLTLN3",
      "FLTLN4": "Subsystem #1|CTLs|Vars|FLTLN4"
    }
    
    self.fltln_dict= { 
      signal: { "path": path, "object": casefx.get_signal( path )  } 
      for signal, path in self.fltln_signals.items() 
    }
    
    
  
  
  def push_button( self, element, time_delay= 0.1 ):    
    element.position= 1
    time.sleep( time_delay )
    element.position= 0
    time.sleep( time_delay )


  def checkpoint_sim( self ):
    
    print( "----------CheckPoint!----------" )
  
    self.flt_bt.position= 0
    self.flt_Case10_bt.position= 0
    self.flt_duration_sld.value= 0.1
    self.flt_location.position= 1

    for ln in self.line_length.values(): ln.value= 50
    for res in self.resistance.values(): res.value= 1
    for sw in self.flt_tp.values(): sw.position= 0
    for flt10 in self.flt10.values(): flt10.value= 0

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


  def evol_flt( self, FLT10_1, FLT10_2 ):

    for i, x in enumerate( [ FLT10_1, FLT10_2 ] ):
      flt10= self.flt10[ list( self.flt10.keys() )[i] ]
      if x == "AG": flt10.value= 1
      elif x == "BG": flt10.value= 2
      elif x == "CG": flt10.value= 4
      elif x == "AB" or x == "BA": flt10.value= 8
      elif x == "BC" or x == "CB": flt10.value= 16
      elif x == "CA" or x == "AC": flt10.value= 32
      elif x == "ABG" or x == "BAG": flt10.value= 9
      elif x == "ACG" or x == "CAG": flt10.value= 33
      elif x == "BCG" or x == "CBG": flt10.value= 18
      elif x == "ABCG": flt10.value= 17

      print( f"\n++++++++++ Fault Evolution= FLT10_1: { x }= { flt10.value } ++++++++\n" )

    
    
  def get_fltln_data( self, caso, flt_loc ):
      
    e_fltln= [ f for f in self.fltln_dict if f[-1] == str( flt_loc ) ][0]                           # 'flt_loc' defines the fault location in the actual case, so just the 'fltln_dict' field is computed
    print( f" E_FLTLN= { e_fltln }" )
    data= self.fltln_dict[ e_fltln ][ "object" ].get_data()
    time= self.fltln_dict[ e_fltln ][ "object" ].get_time_data()
    df= pd.DataFrame( list ( zip( data, time ) ), columns= [ "data", "f_time" ] )
    # self.fltln_dict[ e_fltln ][ "df" ]= df
    flt= df.loc[ df[ 'data' ] > 0, 'f_time' ]                                                       # This number changes depending on the fault type, but always is '> 0' if a fault is applied
    self.fltln_dict[ e_fltln ][ f"Caso_{ caso }" ]= {}
    self.fltln_dict[ e_fltln ][ f"Caso_{ caso }" ][ "f_trip_time" ]= float( flt.iloc[0] ) if not flt.empty else 0
  
    # for i in self.fltln_dict:                                                                     # In case of multiple fault location at the same time
    #   if i == e_fltln:
    #     data= self.fltln_dict[ i ][ "object" ].get_data()
    #     time= self.fltln_dict[ i ][ "object" ].get_time_data()
    #     df= pd.DataFrame( list ( zip( data, time ) ), columns= [ "data", "f_time" ] )
    #     self.fltln_dict[ e_fltln ][ f"Caso_{ caso }" ][ "df" ]= df
    #     self.fltln_dict[ e_fltln ][ f"Caso_{ caso }" ][ "f_trip_time" ]= list( df[ df[ 'data' ] == 1 ][ 'f_time' ] )[0]
      
    return self.fltln_dict[ e_fltln ][ f"Caso_{ caso }" ][ "f_trip_time" ]
     
  
  
  def get_goose_data( self, caso, f_trip_time= 0 ):   
      
    oper= []
    for i in self.goose_dict:
      data= self.goose_dict[ i ][ "object" ].get_data()
      time= self.goose_dict[ i ][ "object" ].get_time_data()
      df= pd.DataFrame( list ( zip( data, time ) ), columns= [ "data", "g_time" ] )
      self.goose_dict[ i ][ f"Caso_{ caso }" ]= {}
      self.goose_dict[ i ][ f"Caso_{ caso }" ][ "df" ]= df
      flt= df.loc[ df[ 'data' ] == 1, 'g_time' ]    
      self.goose_dict[ i ][ f"Caso_{ caso }" ][ "g_trip_time" ]= float( flt.iloc[0] ) if not flt.empty else 0
      # self.goose_dict[ i ][ f"Caso_{ caso }" ][ "g_trip_time" ]= list( df[ df[ 'data' ] == 1 ][ 'g_time' ] )[0]
      diff_Flt_tripTime= self.goose_dict[ i ][ f"Caso_{ caso }" ][ "g_trip_time" ] - f_trip_time
      self.goose_dict[ i ][ f"Caso_{ caso }" ][ "diff_Flt_tripTime" ]= float( diff_Flt_tripTime ) if not flt.empty else 0
      
      oper.append( self.goose_dict[ i ][ f"Caso_{ caso }" ][ "diff_Flt_tripTime" ] )
      
    print( f"\n\n{ oper }\n" )
    
    return oper
        
      
      
     
      
     
      
     
      
     
            
  
        
  




  
      




