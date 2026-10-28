# -*- coding: utf-8 -*-
import time
from pathlib import Path
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
import rtds.rscadfx
import numpy as np
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
      "g__Pickup_Z1": "Subsystem #1|GTNET|GTNET1|g__Pickup_Z1",
      "posC110_A": "Subsystem #1|CTLs|Vars|posC110_A",
      "posC110_B": "Subsystem #1|CTLs|Vars|posC110_B",
      "posC110_C": "Subsystem #1|CTLs|Vars|posC110_C",
      "posC010_A": "Subsystem #1|CTLs|Vars|posC010_A",
      "posC010_B": "Subsystem #1|CTLs|Vars|posC010_B",
      "posC010_C": "Subsystem #1|CTLs|Vars|posC010_C",
    }    
    
    self.goose_dict= { 
      signal: { 
        "path": path, 
        "object": casefx.get_signal( path ), 
        "cases": {}
        } 
      for signal, path in self.goose_signals.items() 
    }
    
    self.fltln_signals= {
      "FLTLN1": "Subsystem #1|CTLs|Vars|FLTLN1",
      "FLTLN2": "Subsystem #1|CTLs|Vars|FLTLN2",
      "FLTLN3": "Subsystem #1|CTLs|Vars|FLTLN3",
      "FLTLN4": "Subsystem #1|CTLs|Vars|FLTLN4"
    }
    
    self.fltln_dict= { 
      signal: { "path": path, "object": casefx.get_signal( path ), "cases": {} } 
      for signal, path in self.fltln_signals.items() 
    }
    
    self.calc_vars= {
      "g_trip_time": self.calc_g_trip_time,
      "diff_Flt_tripTime": self.calc_diff_flt_trip_time,
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


  def fault_location( self, pto_falla ):
    self.flt_location.position= self.flt_loc[ pto_falla ]
    print( f"Fault Location= { pto_falla } -- { self.flt_loc[ pto_falla ] }" )
    print( f"+++ Fault Location Val= { self.flt_location.value }" )


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

      print( f"\n++++++++++ Evolving Fault: FLT10_1 -> { x }= { flt10.value } ++++++++\n" )

    
    
  def get_fltln_data( self, caso, flt_loc ):
      
    e_fltln= [ f for f in self.fltln_dict if f[-1] == str( flt_loc ) ][0]                           # 'flt_loc' defines the fault location in the actual case, so just the 'fltln_dict' field is computed
    print( f" E_FLTLN= { e_fltln }" )
    
    data= self.fltln_dict[ e_fltln ][ "object" ].get_data()
    time= self.fltln_dict[ e_fltln ][ "object" ].get_time_data()
    
    df= pd.DataFrame( { 
        "data": data, 
        "f_time": time 
    } )
    
    flt= df.loc[ df[ 'data' ] > 0, 'f_time' ]                                                       # This number changes depending on the fault type, but always is '> 0' if a fault is applied
    
    self.fltln_dict[ e_fltln ][ "cases" ][ f"Caso_{ caso }" ]= { "f_trip_time": float( flt.iloc[0] ) if not flt.empty else 0 }
  
    # for i in self.fltln_dict:                                                                     # In case of multiple fault location at the same time
    #   if i == e_fltln:
    #     data= self.fltln_dict[ i ][ "object" ].get_data()
    #     time= self.fltln_dict[ i ][ "object" ].get_time_data()
    #     df= pd.DataFrame( list ( zip( data, time ) ), columns= [ "data", "f_time" ] )
    #     self.fltln_dict[ e_fltln ][ "cases" ][ f"Caso_{ caso }" ][ "df" ]= df
    #     self.fltln_dict[ e_fltln ][ "cases" ][ f"Caso_{ caso }" ][ "f_trip_time" ]= list( df[ df[ 'data' ] == 1 ][ 'f_time' ] )[0]
      
    return self.fltln_dict[ e_fltln ][ "cases" ][ f"Caso_{ caso }" ][ "f_trip_time" ]
     
  
  
  # def get_goose_data( self, caso, f_trip_time= 0 ):   
      
  #   oper= []
  #   for i in self.goose_dict:
  #     data= self.goose_dict[ i ][ "object" ].get_data()
  #     time= self.goose_dict[ i ][ "object" ].get_time_data()
  #     df= pd.DataFrame( list ( zip( data, time ) ), columns= [ "data", "g_time" ] )
  #     self.goose_dict[ i ][ "cases" ][ f"Caso_{ caso }" ]= {}
  #     self.goose_dict[ i ][ "cases" ][ f"Caso_{ caso }" ][ "df" ]= df
  #     flt= df.loc[ df[ 'data' ] == 1, 'g_time' ]    
  #     self.goose_dict[ i ][ "cases" ][ f"Caso_{ caso }" ][ "g_trip_time" ]= float( flt.iloc[0] ) if not flt.empty else 0
  #     diff_Flt_tripTime= self.goose_dict[ i ][ "cases" ][ f"Caso_{ caso }" ][ "g_trip_time" ] - f_trip_time
  #     self.goose_dict[ i ][ "cases" ][ f"Caso_{ caso }" ][ "diff_Flt_tripTime" ]= float( diff_Flt_tripTime ) if not flt.empty else 0
      
  #     oper.append( self.goose_dict[ i ][ "cases" ][ f"Caso_{ caso }" ][ "diff_Flt_tripTime" ] )
      
  #   print( f"\n\n{ oper }\n" )
    
  #   return oper
  

  def get_goose_data( self, caso, f_trip_time= 0 ):

    caso= f"Caso_{ caso }"
    oper= []

    for signal, goose in self.goose_dict.items():

      data= goose[ "object" ].get_data()
      time= goose[ "object" ].get_time_data()
      
      df= pd.DataFrame( { "data": data, "g_time": time } )
      
      goose[ "cases" ][ caso ]= { "df": df }
      case_data= goose[ "cases" ][ caso ]

      for calc_var, calc_method in self.calc_vars.items():
        case_data[ calc_var ]= calc_method( f_trip_time= f_trip_time, **case_data )

      oper.append( case_data[ "diff_Flt_tripTime" ] )
      
    return oper
         
  
  def calc_g_trip_time( self, **case_data ):
    df= case_data[ "df" ]
    flt= df.loc[ df[ "data" ] == 1, "g_time" ]
    
    return float( flt.iloc[0] ) if not flt.empty else 0


  def calc_diff_flt_trip_time( self, **case_data ):
    g_trip_time= case_data[ "g_trip_time" ]
    f_trip_time= case_data[ "f_trip_time" ]
    
    return g_trip_time - f_trip_time if g_trip_time else 0
  
  
    
      
  def export_to_excel_goose_results( self, goose_summary_df, exc_cases ):

    dateNtime= time.strftime( '%d%m%Y_%H%M', time.localtime( time.time() ) )
    file_name= f"output_D0008_21__{ dateNtime }.xlsx"
    
    file_exists= Path( file_name ).exists()    
    kwargs= { 
      "engine": "openpyxl",
      "mode": "a" if file_exists else "w" 
    }
    
    if file_exists: kwargs[ "if_sheet_exists" ]= "replace"                              # "overlay"

    with pd.ExcelWriter( file_name, **kwargs ) as writer:     
      
      start_col, start_row= 1, 1
      
      # summary sheet
      goose_summary_df.to_excel( writer, sheet_name= "Summary", startrow= start_row, startcol= start_col, index= True )
    
      for caso in exc_cases:
          
        df= pd.DataFrame.from_dict(
          {
            goose_signal: {
              key: value
              for key, value in signal_data[ "cases" ][ caso ].items()
              if key != "df"
            }
            for goose_signal, signal_data in self.goose_dict.items()
          },
          orient="index",
        )
        
        df.to_excel( writer, sheet_name= caso, startrow= start_row, startcol= start_col, index= True )

      
  
  def export_json( self ):
    
    import copy
    import json
    
    goose_dict_c= copy.deepcopy( self.goose_dict )

    for i in goose_dict_c:
      goose_dict_c[ i ][ "object" ]= '0'
      print( goose_dict_c[ i ][ "object" ] )

    np.save( "goose_dict.npy", goose_dict_c )
    # im_goose_dict= np.load( "goose_dict.npy", allow_pickle= True ).item()

    for i in goose_dict_c:
      for j in goose_dict_c[ i ][ 'cases' ].values():
        j[ 'df_dict' ]= j[ 'df' ].to_dict( orient= 'list' )
        j.pop( 'df', None )
        print( f"{ i }  -->  { j.keys() }" )

    json.dump( goose_dict_c, open( "goose_dict.json", "w" ) )                 # Export
    # im_goose_dict_json= json.load( open( "goose_dict.json" ) )                # Import

     

  def Dist_prot( self, casefx, app ):
    
    # Read the Excel file that contains the test cases
    prot_fcn= "21-21POTT-87L-67NCD"
    usecols="A:G"
    nrows= 16 
    df_dir= r"C:\Archivos_JM\Validacion_Firmware_Relays\Def_Pruebas_Prot_Dist__D008.xlsx"

    df= pd.read_excel( df_dir, sheet_name= prot_fcn, index_col= "Caso", usecols= usecols, nrows= nrows )
    print( df.head )
    goose_data= []

    
    for caso in df.index:                           # list( range( 1, 5 ) ):      df.index
      
      print( f"""
      &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
      
      Executing Case= { caso }
      
      &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
      \n""" )     
      
      if df.Enable[ caso ] == 0:
        print( f"----- Case { caso } Ommitted -----      \n")
        continue
      
      
      pto_falla= df.PtoFalla[ caso ]
      r_falla= df.RFalla[ caso ]
      dist= df.DistPcnt[ caso ]
      tf= df.TFalla[ caso ]
      
      self.fault_res( r_falla, pto_falla )
      self.fault_dist( dist, caso, pto_falla )
      self.fault_dur( tf )
      self.fault_location( pto_falla )
      print( f"Fault Location Main: {  self.flt_location.value  }    \n" )
      
      if caso == 10: 
        FLT10_1, FLT10_2= df.TipoFalla[ caso ].split( '-' )
        self.evol_flt( FLT10_1, FLT10_2 )
      else:
        tp= df.TipoFalla[ caso ]
        self.fault_type( tp )
      
      casefx.compile()
      casefx.run()
      time.sleep( 1 )
      casefx.update_plots()
      
      time.sleep( 3 )
      
      if caso == 10:
        self.push_button( self.flt_Case10_bt ) 
        # time.sleep( float( tf ) )           
        # self.fault_type( tp, 0 )                  
        # self.fault_type( tp2 )                    
        # self.push_button( self.flt_bt )     
        # time.sleep( 3 )
        
      elif caso == 11:  
        self.push_button( self.flt_bt )
        time.sleep( 0.2 )
        self.push_button( self.Opn_DSs[ "Opn_DS_LN2_Bus1_bt" ] ) 
        # self.push_button( self.DSs[ "Opn_DS_LA127_bt" ] )                    # Para el caso 'IntyMedio_0'
        
      elif caso == 12:  
        self.push_button( self.flt_bt )
        time.sleep( 0.2 )      
        self.push_button( self.Opn_DSs[ "Opn_DS_LN2_Bus2_bt" ] ) 
        # self.push_button( self.DSs[ "Opn_DS_LB127" ] )                       # Para el caso 'IntyMedio_0'           

      else: self.push_button( self.flt_bt )

      f_trip_time= self.get_fltln_data( caso, self.flt_loc[ pto_falla ] )
      
      goose_data_case= self.get_goose_data( caso, f_trip_time )
      goose_data.append( goose_data_case )
      # time.sleep( 6 )                   
      
      print( f"----- Case { caso } executed successfully! ----    \n" )
      app.print_message( f"----- Case { caso } executed successfully! ----    \n" )  
      
      casefx.stop()    
      self.checkpoint_sim()
      
      time.sleep( 1 )                           # CB Ready Supervision Time gap
        
    
    goose_data_df2= pd.DataFrame( np.transpose( goose_data ), self.goose_signals ).T
    print( f"\n -------- Goose_data_df: \n { goose_data_df2 } \n" )



  def goose_summary( self, goose_dict ):
    exc_cases= list( next( iter( goose_dict.values() ) )[ "cases" ].keys() )
    goose_summary_df= pd.DataFrame( 
      { g_signal: 
        [ case[ 'diff_Flt_tripTime' ] for i, case in signal_dt[ 'cases' ].items() ] 
        for g_signal, signal_dt in goose_dict.items() 
      }, index= exc_cases )
    
    print( f"\n -------- Goose_summary_df: \n { goose_summary_df }" )
    self.export_to_excel_goose_results( goose_summary_df, exc_cases )


  






"""
goose_dict
└── signal
    ├── path
    ├── object
    └── cases
        ├── Caso_1
        │   ├── df
        │   ├── g_trip_time
        │   ├── diff_Flt_tripTime
        │   └── ...
        │
        ├── Caso_2
        │   ├── df
        │   ├── g_trip_time
        │   ├── diff_Flt_tripTime
        │   └── ...
        │
        └── ...    
     
"""
     
      
     
            
  
        
  




  
      




