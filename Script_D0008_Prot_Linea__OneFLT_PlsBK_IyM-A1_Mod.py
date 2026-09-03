# -*- coding: utf-8 -*-
import rtds.rscadfx
import time
import numpy as np
import pandas as pd
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
from rtds.rscadfx import RSCADError
from valFirm_functions import RTDSModel

# OneFLT: una sola l�gica de fallas y se utiliza un selector para definir la ubicaci�n de la falla
# PlsBK: Se operan los interruptores con pulsadores, con l�gica de operaci�n y memoria
# IyM-A1: Configuraci�n Interruptor y Medio en A1
# Mod: Modularizado. Todas las funciones, creaci�n de objetos, variables y Checkpoint est�n definidas en el script "valFirm_functions.py"
# Casos RSCAD:
# - Template__RTDS_IntyMedio
    

# Read the Excel file that contains the test cases
df= pd.read_excel( "C:/Archivos_JM/Validacion_Firmware_Relays/Def_Pruebas_Prot_Dist__D008.xlsx", sheet_name= "21-21POTT-87L-67NCD", index_col= "Caso", usecols='A:G', nrows= 17 )
print( df.head )
  
try:
  
  # Objects  
  vars= RTDSModel()

  # app.connect()
  with vars.get_connection() as app:
    
    try:

      casefx= app.open_case( r"C:\RSCAD\RTDS_USER_FX\fileman\Validacion_Firmware_Relays\D008__Template__RTDS__IntyMedio\D008__Template__RTDS__IntyMedio.rtfx" )
      
      vars.init_vars( casefx )
      casefx.settings.starting_rack= 2
      casefx.settings.set_plot_window_size( 0.2 )
      casefx.compile()          
      
      
      for caso in list( range( 8,13 ) ):                           #list( range( 1, 5 ) ):      df.index
        
        print( f"""
        &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        
        Executing Case= { caso }
        
        &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        \n""" )     
        
        if df.Enable[ caso ] == 0:
          print( f"----- Case { caso } Ommited -----      \n")
          continue
        
        pto_falla= df.PtoFalla[ caso ]
        r_falla= df.RFalla[ caso ]
        dist= df.DistPcnt[ caso ]
        tf= df.TFalla[ caso ]
        
        vars.fault_res( r_falla, pto_falla )
        vars.fault_dist( dist, caso, pto_falla )
        vars.fault_dur( caso )
        vars.flt_location.position= vars.flt_loc[ pto_falla ]
        print( f"Fault Location: { pto_falla } -- { vars.flt_loc[ pto_falla ] }    \n" )
        
        if caso == 10: 
          tp, tp2= df.TipoFalla[ caso ].split( '-' )
        else:
          tp= df.TipoFalla[ caso ]
                
        vars.fault_type( tp )
        
        casefx.compile()
        casefx.run()
        time.sleep( 1 )
        casefx.update_plots()
        
        time.sleep( 3 )
        
        vars.push_button( vars.flt_bt )
        
        if caso == 10:
          time.sleep( float( tf ) )
          vars.fault_type( tp, 0 )                  
          vars.fault_type( tp2 )                    
          vars.push_button( vars.flt_bt )     
          time.sleep( 3 )
          
        elif caso == 11:  
          time.sleep( 0.2 )
          vars.push_button( vars.DSs[ "Opn_DS_LN2_Bus1_bt" ] ) 
          
        elif caso == 12:  
          time.sleep( 0.2 )      
          vars.push_button( vars.DSs[ "Opn_DS_LN2_Bus2_bt" ] )           
              
        time.sleep( 6 )                   
        
        print( f"----- Case { caso } executed successfully! ----    \n" )
        app.print_message( f"----- Case { caso } executed successfully! ----    \n" )  
        
        casefx.stop()    
        vars.checkpoint_sim()
        
        time.sleep( 6 )                           # CB Ready Supervision Time gap
          
      



    except RSCADError as re:  
      print( f"""
      &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
      
      RSCADError: 
      { re }
      
      &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
      \n""" )
      pass

    except Exception as e:      
      print( f"e= { e }" )
      
    finally:
      # casefx.close()
      # print( "++++++++++  Case Closed    \n" )
      app.print_message( "++ Conection with RSCAD Closed ++    \n" )
      # app.disconnect( terminate= False )

except Exception as ee:
  # self._log_write(f"Error crítico en la ejecución: {e}")
  # raise  # Relanzamos para que la API sepa que hubo error
  print( f"ee= { ee }" )
  app.disconnect( terminate= False )

finally:
  # GUARDAMOS EL EXCEL DE RESULTADOS
  # self._log_write(f"Guardando reporte final en: {report_path}")
  # df_plan.to_excel(report_path, index=False)
  # app.disconnect( terminate= True )
  print( "++ Conection with RSCAD Closed ++    \n" )

