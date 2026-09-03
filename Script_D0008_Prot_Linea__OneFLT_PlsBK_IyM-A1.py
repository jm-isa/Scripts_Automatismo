import rtds.rscadfx
import time
import numpy as np
import pandas as pd
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
from rtds.rscadfx import RSCADError


# OneFLT: una sola l�gica de fallas y se utiliza un selector para definir la ubicaci�n de la falla
# PlsBK: Se operan los interruptores con pulsadores, con l�gica de operaci�n y memoria
# IyM-A1: Configuraci�n Interruptor y Medio en A1


def checkpoint_sim():
  
  print( "----------CheckPoint!----------" )

  flt_bt.position= 0
  flt_duration_sld.value= 0.1
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
  
  Cls3_C110_bt.position= 1
  Cls3_C110_bt.position= 0
  
  Cls3_C010_bt.position= 1
  Cls3_C010_bt.position= 0
  
  Cls_DS_LN2_Bus1_bt.position= 1
  Cls_DS_LN2_Bus1_bt.position= 0
  
  Cls_DS_LN2_Bus2_bt.position= 1
  Cls_DS_LN2_Bus2_bt.position= 0
    
  time.sleep( 1 )
  

def fault_type( tp, value= 1 ):
  
  # tp= df.TipoFalla[ caso ]
  # tp= df.TipoFalla[ caso ].split( '-' )[0] if tp.find( "-" ) else tp
  # flt_tp= f"{ tp }_{ pto_falla }"
  
  match tp:
    case "AG": ag.position= value
    case "BG": bg.position= value
    case "CG": cg.position= value    
    case "ABG": ag.position, bg.position= value, value
    case "ACG": ag.position, cg.position= value, value
    case "BCG": bg.position, cg.position= value, value      
    case "AB": ab.position= value
    case "BC": bc.position= value
    case "CA": ca.position= value    
    case "ABCG": ag.position, bg.position, cg.position= value, value, value

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

df= pd.read_excel( "C:/Archivos_JM/Validacion_Firmware_Relays/Def_Pruebas_Prot_Dist__D008.xlsx", sheet_name= "21-21POTT-87L-67NCD", index_col= "Caso", usecols='A:G', nrows= 17 )
print( df.head )


app= rtds.rscadfx.remote_connection()
  
try:
  
  app.connect()
  casefx= app.open_case( r"C:\RSCAD\RTDS_USER_FX\fileman\Validacion_Firmware_Relays\D008__Template__RTDS__IntyMedio\D008__Template__RTDS__IntyMedio.rtfx" )
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
      
  Opn3_C110_bt= casefx.get_object_by_name( "Opn3_C110", BUTTON )
  Opn3_C010_bt= casefx.get_object_by_name( "Opn3_C010", BUTTON )    
  Opn_DS_LN2_Bus1_bt= casefx.get_object_by_name( "Opn_DS_LN2_Bus1", BUTTON )
  Opn_DS_LN2_Bus2_bt= casefx.get_object_by_name( "Opn_DS_LN2_Bus2", BUTTON )
    
  Cls3_C110_bt= casefx.get_object_by_name( "Cls3_C110", BUTTON )
  Cls3_C010_bt= casefx.get_object_by_name( "Cls3_C010", BUTTON ) 
  Cls_DS_LN2_Bus1_bt= casefx.get_object_by_name( "Cls_DS_LN2_Bus1", BUTTON )
  Cls_DS_LN2_Bus2_bt= casefx.get_object_by_name( "Cls_DS_LN2_Bus2", BUTTON )  
    
  # plot_ctn= casefx.get_object_by_name( "Fault Bus", PLOT_CONTAINER )
  
  flt_loc= {
    "LN1": 1,
    "LN2": 2,
    "LN3": 3,
    "LN4": 4    
  }
  
  # volts= casefx.get_signal( "Subsystem #1|Node Voltages|S1) N3A" )
      
      

  
  for caso in list( range( 1,2 ) ):                           #list( range( 1, 5 ) ):      df.index
    
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
      # ag.position= 1   
      tp, tp2= df.TipoFalla[ caso ].split( '-' )
    else:
      tp= df.TipoFalla[ caso ]
            
    fault_type( tp )
    
    casefx.compile()
    casefx.run()
    time.sleep( 1 )
    casefx.update_plots()
    
    time.sleep( 3 )
    
    flt_bt.position= 1
    flt_bt.position= 0

    
    if caso == 10:
      time.sleep( float( df.TFalla[ caso ] ) )
      fault_type( tp, 0 )                  # ag.position= 0
      fault_type( tp2 )                     # bg.position= 1
      flt_bt.position= 1
      flt_bt.position= 0      
      time.sleep( 3 )
      
    elif caso == 11:  
      time.sleep( 0.2 )
      Opn_DS_LN2_Bus1_bt.position= 1
      Opn_DS_LN2_Bus1_bt.position= 0
      
    elif caso == 12:  
      time.sleep( 0.2 )      
      Opn_DS_LN2_Bus2_bt.position= 1
      Opn_DS_LN2_Bus2_bt.position= 0
      
          
    time.sleep( 6 )                   
    
    print( f"----- Case { caso } executed successfully! ----    \n" )
    app.print_message( f"----- Case { caso } executed successfully! ----    \n" )  
    
    casefx.stop()    
    checkpoint_sim()
    
    time.sleep( 6 )                           # CB Ready Supervision Time gap
      
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
