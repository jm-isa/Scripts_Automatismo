import rtds.rscadfx
import time
import numpy as np
import pandas as pd
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
from rtds.rscadfx import RSCADError


def checkpoint_sim():

  fault_bt.position= 0
  resistance_sld.value= 1
  flt_loc_sld.value= 50
  flt_duration_sld.value= 0
  
  ag_LN1.position= 0
  bg_LN1.position= 0
  cg_LN1.position= 0
  ab_LN1.position= 0
  bc_LN1.position= 0
  ca_LN1.position= 0
  
  BRK_B1_A.position= 1
  BRK_B1_B.position= 1
  BRK_B1_C.position= 1
  BRK_B2_A.position= 1
  BRK_B2_B.position= 1
  BRK_B2_C.position= 1
  
  time.sleep( 1 )
  

def fault_type( flt_tp ):
  
  flt_tp= df.TipoFalla[ caso ].split( '-' )[0] if flt_tp.find( "-" ) else flt_tp
  
  match flt_tp:
    case "AG_LN1": ag_LN1.position= 1
    case "BG_LN1": bg_LN1.position= 1
    case "CG_LN1": cg_LN1.position= 1
    
    case "ABG_LN1": ag_LN1.position, bg_LN1.position= 1, 1
    case "ACG_LN1": ag_LN1.position, cg_LN1.position= 1, 1
    case "BCG_LN1": bg_LN1.position, cg_LN1.position= 1, 1
      
    case "AB_LN1": ab_LN1.position= 1
    case "BC_LN1": bc_LN1.position= 1
    case "CA_LN1": ca_LN1.position= 1
    
    case "ABCG_LN1": ag_LN1.position, bg_LN1.position, cg_LN1.position= 1, 1, 1
    
  print( f"Fault Type= { flt_tp }" )
  

def fault_res( caso ):
  
  resistance_sld.value= float( df.RFalla[ caso ] )
  
  print( f"RFalla= { resistance_sld.value }" )
    

def fault_dist( dist ):
  
  flt_loc_sld.value= int( dist )
  
  print( f"Fault Distance= { dist }" )


def fault_dur( time ):
  
  flt_duration_sld.value= float( time )
  
  print( f"Fault Duration= { time }" )
 
    

# Read the Excel file that contains the test cases

df= pd.read_excel( "C:/Archivos_JM/Validacion_Firmware_Relays/Def_Pruebas_Prot_Dist__D008.xlsx", sheet_name= "Hoja1", index_col= "Caso", usecols='A:M', nrows= 17 )
print( df.head )


app= rtds.rscadfx.remote_connection()
  
try:
  
  app.connect()
  

  casefx= app.open_case( r"D:\mis documentos\RSCAD\RTDS_USER_FX\fileman\Validacion_Firmware_Relays\AC Transmission Line__Script\AC_Transmission_Line.rtfx" )
  casefx.settings.starting_rack= 2
  casefx.settings.set_plot_window_size( 2 )
  casefx.compile()

  
  
  # Objects
  
  # Line1 (DUT)
  flt_loc_sld= casefx.get_object_by_name( "Length_LN1", SLIDER )
  resistance_sld= casefx.get_object_by_name( "Ron_LN1", SLIDER )
  flt_duration_sld= casefx.get_object_by_name( "FLTDUR_LN1", SLIDER )
  fault_bt= casefx.get_object_by_name( "FLTLN1", BUTTON )
  ag_LN1= casefx.get_object_by_name( "AG_LN1", SWITCH )
  bg_LN1= casefx.get_object_by_name( "BG_LN1", SWITCH )
  cg_LN1= casefx.get_object_by_name( "CG_LN1", SWITCH )
  ab_LN1= casefx.get_object_by_name( "AB_LN1", SWITCH )
  bc_LN1= casefx.get_object_by_name( "BC_LN1", SWITCH )
  ca_LN1= casefx.get_object_by_name( "CA_LN1", SWITCH )
  
  BRK_B1_A= casefx.get_object_by_name( "BRK_B1_A", SWITCH )
  BRK_B1_B= casefx.get_object_by_name( "BRK_B1_B", SWITCH )
  BRK_B1_C= casefx.get_object_by_name( "BRK_B1_C", SWITCH )
  BRK_B2_A= casefx.get_object_by_name( "BRK_B2_A", SWITCH )
  BRK_B2_B= casefx.get_object_by_name( "BRK_B2_B", SWITCH )
  BRK_B2_C= casefx.get_object_by_name( "BRK_B2_C", SWITCH )
  
  plot_ctn= casefx.get_object_by_name( "Fault Bus", PLOT_CONTAINER )
  
  # volts= casefx.get_signal( "Subsystem #1|Node Voltages|S1) N3A" )
      
      
     
      
  
  for caso in df.index:                           #list( range( 1, 5 ) ):
    
    print( f"""
    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    
    Executing Case= { caso }
    
    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    """ )
      
   
    fault_res( caso )
    fault_dist( df.DistPcnt[ caso ] )
    fault_type( df.TipoFalla[ caso ] )  
    fault_dur( df.TFalla[ caso ] )
    
    casefx.compile()
    casefx.run()
    time.sleep( 0.01 )
    fault_bt.position= 1
    fault_bt.position= 0
    app.print_message( f"----- Case { caso } executed successfully! ----" )  
    casefx.stop()    
    checkpoint_sim()
    
    time.sleep( 2 )
      
  print( "Conection with RSCAD Closed" )



except RSCADError as e:  
  print( f"""
  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  
  RSCADError: 
  { e }
  
  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  """ )
  pass
  
finally:
  app.disconnect( terminate= False )
