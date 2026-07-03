import rtds.rscadfx
import time
import numpy as np
import pandas as pd
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
from rtds.rscadfx import RSCADError


def checkpoint_sim():

  # Línea 1
  fault_bt_LN1.position= 0
  flt_duration_sld_LN1.value= 0
  flt_loc_sld_LN1.value= 50
  resistance_sld_LN1.value= 1

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
  
  # Línea 2
  fault_bt_LN2.position= 0
  flt_duration_sld_LN2.value= 0
  flt_loc_sld_LN2.value= 50
  resistance_sld_LN2.value= 1
  
  ag_LN2.position= 0
  bg_LN2.position= 0
  cg_LN2.position= 0
  ab_LN2.position= 0
  bc_LN2.position= 0
  ca_LN2.position= 0

  # Línea 3
  fault_bt_LN3.position= 0
  flt_duration_sld_LN3.value= 0
  flt_loc_sld_LN3.value= 50
  resistance_sld_LN3.value= 1

  ag_LN3.position= 0
  bg_LN3.position= 0
  cg_LN3.position= 0
  ab_LN3.position= 0
  bc_LN3.position= 0
  ca_LN3.position= 0
  
  time.sleep( 1 )
  

def fault_type( caso, pto_falla ):
  
  tp= df.TipoFalla[ caso ]
  tp= df.TipoFalla[ caso ].split( '-' )[0] if tp.find( "-" ) else tp
  flt_tp= f"{ tp }_{ pto_falla }"
  
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
    
    case "AG_LN2": ag_LN2.position= 1
    case "BG_LN2": bg_LN2.position= 1
    case "CG_LN2": cg_LN2.position= 1    
    case "ABG_LN2": ag_LN2.position, bg_LN2.position= 1, 1
    case "ACG_LN2": ag_LN2.position, cg_LN2.position= 1, 1
    case "BCG_LN2": bg_LN2.position, cg_LN2.position= 1, 1      
    case "AB_LN2": ab_LN2.position= 1
    case "BC_LN2": bc_LN2.position= 1
    case "CA_LN2": ca_LN2.position= 1    
    case "ABCG_LN2": ag_LN2.position, bg_LN2.position, cg_LN2.position= 1, 1, 1
    
    case "AG_LN3": ag_LN3.position= 1
    case "BG_LN3": bg_LN3.position= 1
    case "CG_LN3": cg_LN3.position= 1    
    case "ABG_LN3": ag_LN3.position, bg_LN3.position= 1, 1
    case "ACG_LN3": ag_LN3.position, cg_LN3.position= 1, 1
    case "BCG_LN3": bg_LN3.position, cg_LN3.position= 1, 1      
    case "AB_LN3": ab_LN3.position= 1
    case "BC_LN3": bc_LN3.position= 1
    case "CA_LN3": ca_LN3.position= 1    
    case "ABCG_LN3": ag_LN3.position, bg_LN3.position, cg_LN3.position= 1, 1, 1

  print( f"Fault Type= { flt_tp }" )
  

def fault_res( caso, pto_falla ):  
    
  match pto_falla:
    case "LN1": resistance_sld_LN1.value= float( df.RFalla[ caso ] )
    case "LN2": resistance_sld_LN2.value= float( df.RFalla[ caso ] )
    case "LN3": resistance_sld_LN3.value= float( df.RFalla[ caso ] )
    
  print( f"RFalla= { df.RFalla[ caso ] }" )
    

def fault_dist( caso, pto_falla ):
  
  dist= df.DistPcnt[ caso ]
  
  match pto_falla:
    case "LN1": flt_loc_sld_LN1.value= int( dist )
    case "LN2": flt_loc_sld_LN2.value= int( dist )
    case "LN3": flt_loc_sld_LN3.value= int( dist )
  
  print( f"Fault Distance= { dist }" )


def fault_dur( time, pto_falla ):
  
  tf= df.TFalla[ caso ]
  
  match pto_falla:
    case "LN1": flt_duration_sld_LN1.value= float( tf )
    case "LN2": flt_duration_sld_LN2.value= float( tf )
    case "LN3": flt_duration_sld_LN3.value= float( tf )
  
  print( f"Fault Duration= { tf }" )
 
    

# Read the Excel file that contains the test cases

df= pd.read_excel( "C:/Archivos_JM/Validación Firmware Relays/Def_Pruebas_Prot_Dist__D008.xlsx", sheet_name= "Hoja1", index_col= "Caso", usecols='A:M', nrows= 17 )
print( df.head )


app= rtds.rscadfx.remote_connection()
  
try:
  
  app.connect()
  casefx= app.open_case( r"C:\RSCAD\RTDS_USER_FX\fileman\Validacion_Firmware_Relays\AC Transmission Line__Script\AC_Transmission_Line.rtfx" )
  casefx.settings.starting_rack= 2
  casefx.settings.set_plot_window_size( 0.1 )
  casefx.compile()
  
  
  # Objects  
  # Line1
  flt_loc_sld_LN1= casefx.get_object_by_name( "Length_LN1", SLIDER )
  resistance_sld_LN1= casefx.get_object_by_name( "Ron_LN1", SLIDER )
  flt_duration_sld_LN1= casefx.get_object_by_name( "FLTDUR_LN1", SLIDER )
  fault_bt_LN1= casefx.get_object_by_name( "FLT_LN1", BUTTON )
  ag_LN1= casefx.get_object_by_name( "AG_LN1", SWITCH )
  bg_LN1= casefx.get_object_by_name( "BG_LN1", SWITCH )
  cg_LN1= casefx.get_object_by_name( "CG_LN1", SWITCH )
  ab_LN1= casefx.get_object_by_name( "AB_LN1", SWITCH )
  bc_LN1= casefx.get_object_by_name( "BC_LN1", SWITCH )
  ca_LN1= casefx.get_object_by_name( "CA_LN1", SWITCH )
    
  # Line2 
  flt_loc_sld_LN2= casefx.get_object_by_name( "Length_LN2", SLIDER )
  resistance_sld_LN2= casefx.get_object_by_name( "Ron_LN2", SLIDER )
  flt_duration_sld_LN2= casefx.get_object_by_name( "FLTDUR_LN2", SLIDER )
  fault_bt_LN2= casefx.get_object_by_name( "FLT_LN2", BUTTON )
  ag_LN2= casefx.get_object_by_name( "AG_LN2", SWITCH )
  bg_LN2= casefx.get_object_by_name( "BG_LN2", SWITCH )
  cg_LN2= casefx.get_object_by_name( "CG_LN2", SWITCH )
  ab_LN2= casefx.get_object_by_name( "AB_LN2", SWITCH )
  bc_LN2= casefx.get_object_by_name( "BC_LN2", SWITCH )
  ca_LN2= casefx.get_object_by_name( "CA_LN2", SWITCH )
  
  # Line3
  flt_loc_sld_LN3= casefx.get_object_by_name( "Length_LN3", SLIDER )
  resistance_sld_LN3= casefx.get_object_by_name( "Ron_LN3", SLIDER )
  flt_duration_sld_LN3= casefx.get_object_by_name( "FLTDUR_LN3", SLIDER )
  fault_bt_LN3= casefx.get_object_by_name( "FLT_LN3", BUTTON )
  ag_LN3= casefx.get_object_by_name( "AG_LN3", SWITCH )
  bg_LN3= casefx.get_object_by_name( "BG_LN3", SWITCH )
  cg_LN3= casefx.get_object_by_name( "CG_LN3", SWITCH )
  ab_LN3= casefx.get_object_by_name( "AB_LN3", SWITCH )
  bc_LN3= casefx.get_object_by_name( "BC_LN3", SWITCH )
  ca_LN3= casefx.get_object_by_name( "CA_LN3", SWITCH )
  
  BRK_B1_A= casefx.get_object_by_name( "BRK_B1_A", SWITCH )
  BRK_B1_B= casefx.get_object_by_name( "BRK_B1_B", SWITCH )
  BRK_B1_C= casefx.get_object_by_name( "BRK_B1_C", SWITCH )
  BRK_B2_A= casefx.get_object_by_name( "BRK_B2_A", SWITCH )
  BRK_B2_B= casefx.get_object_by_name( "BRK_B2_B", SWITCH )
  BRK_B2_C= casefx.get_object_by_name( "BRK_B2_C", SWITCH )
  
  plot_ctn= casefx.get_object_by_name( "Fault Bus", PLOT_CONTAINER )
  
  flt_bt= {
    "LN1": casefx.get_object_by_name( "FLT_LN1", BUTTON ),
    "LN2": casefx.get_object_by_name( "FLT_LN2", BUTTON ),
    "LN3": casefx.get_object_by_name( "FLT_LN3", BUTTON )    
  }
  
  # volts= casefx.get_signal( "Subsystem #1|Node Voltages|S1) N3A" )
      
      

  
  for caso in list( range( 10, 11 ) ):                           #list( range( 1, 5 ) ):      df.index
    
    print( f"""
    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    
    Executing Case= { caso }
    
    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    """ )     
      
    
    # if caso == 10:      
      
    #   fault_res( caso, pto_falla )
    #   fault_dist( caso, pto_falla )
    #   fault_dur( caso, pto_falla )
    #   ag_LN1.position= 1
      
    #   casefx.compile()
    #   casefx.run()
      
    #   time.sleep( 0.01 )
      
    #   flt_bt[ pto_falla ].position= 1
    #   flt_bt[ pto_falla ].position= 0
      
      
    #   time.sleep( 0.06 )
    #   ag_LN1.position= 0
    #   bg_LN1.position= 1
    #   flt_bt[ pto_falla ].position= 1
    #   flt_bt[ pto_falla ].position= 0      
    #   time.sleep( 0.01 )
      
    #   continue
    
   
    pto_falla= df.PtoFalla[ caso ]
    
    fault_res( caso, pto_falla )
    fault_dist( caso, pto_falla )
    fault_dur( caso, pto_falla )
    
    
    if caso == 10: 
      ag_LN1.position= 1
    else:
      fault_type( caso, pto_falla )
    
    
    casefx.compile()
    casefx.run()
    
    time.sleep( 0.01 )
    
    flt_bt[ pto_falla ].position= 1
    flt_bt[ pto_falla ].position= 0
    
    if caso == 10:
      time.sleep( 0.06 )
      ag_LN1.position= 0
      bg_LN1.position= 1
      flt_bt[ pto_falla ].position= 1
      flt_bt[ pto_falla ].position= 0      
      time.sleep( 0.01 )
      
    
    print( f"----- Case { caso } executed successfully! ----" )
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
