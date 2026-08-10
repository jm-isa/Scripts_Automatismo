# OneFLT: una sola lógica de fallas y se utiliza un selector para definir la ubicación de la falla
# SwBK: Se operan los interruptores con switches manuales, sin lógica de operación de CB


import rtds.rscadfx
import time
import numpy as np
import pandas as pd
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
from rtds.rscadfx import RSCADError


def checkpoint_sim():

  # Línea 1
  flt_bt.position= 0
  flt_duration_sld.value= 0
  flt_location.position= 1

  line_length_sld_LN1.value= 50
  line_length_sld_LN3.value= 50
  line_length_sld_LN4.value= 50

  resistance_sld_LN1.value= 1
  resistance_sld_LN2.value= 1
  resistance_sld_LN3.value= 1
  resistance_sld_LN4.value= 1

  ag.position= 0
  bg.position= 0
  cg.position= 0
  ab.position= 0
  bc.position= 0
  ca.position= 0
      
  BRK_LN1_B1_A.position= 1
  BRK_LN1_B1_B.position= 1
  BRK_LN1_B1_C.position= 1
  BRK_LN1_B2_A.position= 1
  BRK_LN1_B2_B.position= 1
  BRK_LN1_B2_C.position= 1      

  BRK_LN2_B1_A.position= 1
  BRK_LN2_B1_B.position= 1
  BRK_LN2_B1_C.position= 1
  BRK_LN2_B2_A.position= 1
  BRK_LN2_B2_B.position= 1
  BRK_LN2_B2_C.position= 1
  
  time.sleep( 1 )
  

def fault_type( caso ):
  
  tp= df.TipoFalla[ caso ]
  tp= df.TipoFalla[ caso ].split( '-' )[0] if tp.find( "-" ) else tp
  # flt_tp= f"{ tp }_{ pto_falla }"
  
  match tp:
    case "AG": ag.position= 1
    case "BG": bg.position= 1
    case "CG": cg.position= 1    
    case "ABG": ag.position, bg.position= 1, 1
    case "ACG": ag.position, cg.position= 1, 1
    case "BCG": bg.position, cg.position= 1, 1      
    case "AB": ab.position= 1
    case "BC": bc.position= 1
    case "CA": ca.position= 1    
    case "ABCG": ag.position, bg.position, cg.position= 1, 1, 1

  print( f"Fault Type= { tp }" )
  

def fault_res( caso, pto_falla ):  
    
  match pto_falla:
    case "LN1": resistance_sld_LN1.value= float( df.RFalla[ caso ] )
    case "LN2": resistance_sld_LN2.value= float( df.RFalla[ caso ] )
    case "LN3": resistance_sld_LN3.value= float( df.RFalla[ caso ] )
    case "LN4": resistance_sld_LN4.value= float( df.RFalla[ caso ] )
    
  print( f"RFalla= { df.RFalla[ caso ] }" )
    

def fault_dist( caso ):
  
  dist= df.DistPcnt[ caso ]
  
  if caso == 11 or caso == 12:
    line_length_sld_LN1.value= int( dist )

  else:
    match pto_falla:
      case "LN1": line_length_sld_LN1.value= int( dist )
      case "LN3": line_length_sld_LN3.value= int( dist )
      case "LN4": line_length_sld_LN4.value= int( dist )
  
  print( f"Fault Distance= { dist }" )


def fault_dur( caso ):
  
  tf= df.TFalla[ caso ]
  flt_duration_sld.value= float( tf )
  
  print( f"Fault Duration= { tf }" )
 
    

# Read the Excel file that contains the test cases

df= pd.read_excel( "C:/Archivos_JM/Validacion_Firmware_Relays/Def_Pruebas_Prot_Dist__D008.xlsx", sheet_name= "Hoja1", index_col= "Caso", usecols='A:G', nrows= 17 )
print( df.head )


app= rtds.rscadfx.remote_connection()
  
try:
  
  app.connect()
  casefx= app.open_case( r"C:\RSCAD\RTDS_USER_FX\fileman\Validacion_Firmware_Relays\D008__Template__RTDS\D008__Template__RTDS.rtfx" )
  casefx.settings.starting_rack= 2
  casefx.settings.set_plot_window_size( 0.2 )
  casefx.compile()
  
  
  # Objects  
  flt_bt= casefx.get_object_by_name( "FLT", BUTTON )
  flt_duration_sld= casefx.get_object_by_name( "FLTDUR", SLIDER )

  line_length_sld_LN1= casefx.get_object_by_name( "Length_LN1", SLIDER )
  line_length_sld_LN3= casefx.get_object_by_name( "Length_LN3", SLIDER )
  line_length_sld_LN4= casefx.get_object_by_name( "Length_LN4", SLIDER )
  resistance_sld_LN1= casefx.get_object_by_name( "Ron_LN1", SLIDER )
  resistance_sld_LN2= casefx.get_object_by_name( "Ron_LN2", SLIDER )
  resistance_sld_LN3= casefx.get_object_by_name( "Ron_LN3", SLIDER )
  resistance_sld_LN4= casefx.get_object_by_name( "Ron_LN4", SLIDER )
  flt_location= casefx.get_object_by_name( 'FLT_LOC', 'dial' )
  
  ag= casefx.get_object_by_name( "AG", SWITCH )
  bg= casefx.get_object_by_name( "BG", SWITCH )
  cg= casefx.get_object_by_name( "CG", SWITCH )
  ab= casefx.get_object_by_name( "AB", SWITCH )
  bc= casefx.get_object_by_name( "BC", SWITCH )
  ca= casefx.get_object_by_name( "CA", SWITCH )  
  
  BRK_LN1_B1_A= casefx.get_object_by_name( "BRK_LN1_B1_A", SWITCH )
  BRK_LN1_B1_B= casefx.get_object_by_name( "BRK_LN1_B1_B", SWITCH )
  BRK_LN1_B1_C= casefx.get_object_by_name( "BRK_LN1_B1_C", SWITCH )
  BRK_LN1_B2_A= casefx.get_object_by_name( "BRK_LN1_B2_A", SWITCH )
  BRK_LN1_B2_B= casefx.get_object_by_name( "BRK_LN1_B2_B", SWITCH )
  BRK_LN1_B2_C= casefx.get_object_by_name( "BRK_LN1_B2_C", SWITCH )

  BRK_LN2_B1_A= casefx.get_object_by_name( "BRK_LN2_B1_A", SWITCH )
  BRK_LN2_B1_B= casefx.get_object_by_name( "BRK_LN2_B1_B", SWITCH )
  BRK_LN2_B1_C= casefx.get_object_by_name( "BRK_LN2_B1_C", SWITCH )
  BRK_LN2_B2_A= casefx.get_object_by_name( "BRK_LN2_B2_A", SWITCH )
  BRK_LN2_B2_B= casefx.get_object_by_name( "BRK_LN2_B2_B", SWITCH )
  BRK_LN2_B2_C= casefx.get_object_by_name( "BRK_LN2_B2_C", SWITCH )
  
  # plot_ctn= casefx.get_object_by_name( "Fault Bus", PLOT_CONTAINER )
  
  flt_loc= {
    "LN1": 1,
    "LN2": 2,
    "LN3": 3,
    "LN4": 4    
  }
  
  # volts= casefx.get_signal( "Subsystem #1|Node Voltages|S1) N3A" )
      
      

  
  for caso in list( range( 9, 13 ) ):                           #list( range( 1, 5 ) ):      df.index
    
    print( f"""
    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    
    Executing Case= { caso }
    
    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    \n""" )     
    
    if df.Enable[ caso ] == 0:
      print( f"----- Case { caso } Ommited -----      \n")
      continue
    
    pto_falla= df.PtoFalla[ caso ]
    
    fault_res( caso, pto_falla )
    fault_dist( caso )
    fault_dur( caso )
    flt_location.position= flt_loc[ pto_falla ]
    print( f"Fault Location: { pto_falla } -- { flt_loc[ pto_falla ] }    \n" )
    
    if caso == 10: 
      ag.position= 1      
    else:
      fault_type( caso )
    
    
    casefx.compile()
    casefx.run()
    
    # time.sleep( 0.01 )
    time.sleep( 3 )
    
    flt_bt.position= 1
    flt_bt.position= 0

    
    if caso == 10:
      time.sleep( float( df.TFalla[ caso ] ) )
      ag.position= 0
      bg.position= 1
      flt_bt.position= 1
      flt_bt.position= 0      
      time.sleep( 3 )
      
    elif caso == 11:  
      time.sleep( 0.2 )
      BRK_LN2_B1_A.position, BRK_LN2_B1_B.position, BRK_LN2_B1_C.position= 0, 0, 0
      
    elif caso == 12:  
      time.sleep( 0.2 )      
      BRK_LN2_B2_A.position, BRK_LN2_B2_B.position, BRK_LN2_B2_C.position= 0, 0, 0
      
          
    time.sleep( 3 )
    
    print( f"----- Case { caso } executed successfully! ----    \n" )
    app.print_message( f"----- Case { caso } executed successfully! ----    \n" )  
    
    casefx.stop()    
    checkpoint_sim()
    
    time.sleep( 2 )
      
  print( "Conection with RSCAD Closed    \n" )



except RSCADError as e:  
  print( f"""
  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  
  RSCADError: 
  { e }
  
  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
  \n""" )
  pass
  
finally:
  app.disconnect( terminate= False )
