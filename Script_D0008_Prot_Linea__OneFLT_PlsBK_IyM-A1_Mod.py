# -*- coding: utf-8 -*-
import rtds.rscadfx
import time
import copy
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rtds.constants import BUTTON, PLOT_CONTAINER, SLIDER, SWITCH
from rtds.rscadfx import RSCADError

# OneFLT: una sola l�gica de fallas y se utiliza un selector para definir la ubicaci�n de la falla
# PlsBK: Se operan los interruptores con pulsadores, con l�gica de operaci�n y memoria
# IyM-A1: Configuraci�n Interruptor y Medio en A1
# Mod: Modularizado. Todas las funciones, creaci�n de objetos, variables y Checkpoint est�n definidas en el script "valFirm_functions.py"
# Casos RSCAD:
# - Template__RTDS_IntyMedio
    

      

# from valFirm_functions import RTDSModel
# casefx_dir= r"C:\RSCAD\RTDS_USER_FX\fileman\Validacion_Firmware_Relays\D008__Template__RTDS__IntyMedio\D008__Template__RTDS__IntyMedio.rtfx"
from valFirm_functions_0 import RTDSModel
casefx_dir= r"C:\RSCAD\RTDS_USER_FX\fileman\Validacion_Firmware_Relays\D008__Template__RTDS__IntyMedio_0\D008__Template__RTDS__IntyMedio_0.rtfx"
 
try:
  
  # Objects  
  vars= RTDSModel()

  # app.connect()
  with vars.get_connection() as app:
    
    try:

      casefx= app.open_case( casefx_dir )
      
      vars.init_vars( casefx )
      casefx.settings.starting_rack= 2
      casefx.settings.set_plot_window_size( 0.8 )
      vars.checkpoint_sim()
      casefx.compile()    
      
      
      vars.Dist_prot( casefx, app )
      vars.goose_summary( vars.goose_dict )
            



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





