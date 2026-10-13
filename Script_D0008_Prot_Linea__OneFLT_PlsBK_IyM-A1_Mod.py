# -*- coding: utf-8 -*-
import rtds.rscadfx
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
prot_fcn= "21-21POTT-87L-67NCD"
usecols="A:G"
nrows= 17 

df= pd.read_excel( "C:/Archivos_JM/Validacion_Firmware_Relays/Def_Pruebas_Prot_Dist__D008.xlsx", sheet_name= prot_fcn, index_col= "Caso", usecols= usecols, nrows= nrows )
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
      casefx.settings.set_plot_window_size( 0.6 )
      casefx.compile()         
      goose_data= []

      
      for caso in list( range( 1,4 ) ):                           # list( range( 1, 5 ) ):      df.index
        
        print( f"""
        &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        
        Executing Case= { caso }
        
        &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        \n""" )     
        
        if df.Enable[ caso ] == 0:
          print( f"----- Case { caso } Ommited -----      \n")
          continue
        
        if caso == 1: vars.checkpoint_sim()
        
        pto_falla= df.PtoFalla[ caso ]
        r_falla= df.RFalla[ caso ]
        dist= df.DistPcnt[ caso ]
        tf= df.TFalla[ caso ]
        
        vars.fault_res( r_falla, pto_falla )
        vars.fault_dist( dist, caso, pto_falla )
        vars.fault_dur( tf )
        vars.flt_location.position= vars.flt_loc[ pto_falla ]
        print( f"Fault Location: { pto_falla } -- { vars.flt_loc[ pto_falla ] }    \n" )
        
        if caso == 10: 
          FLT10_1, FLT10_2= df.TipoFalla[ caso ].split( '-' )
          vars.evol_flt( FLT10_1, FLT10_2 )
        else:
          tp= df.TipoFalla[ caso ]
          vars.fault_type( tp )
        
        casefx.compile()
        casefx.run()
        time.sleep( 1 )
        casefx.update_plots()
        
        time.sleep( 3 )
        
        if caso == 10:
          vars.push_button( vars.flt_Case10_bt ) 
          # time.sleep( float( tf ) )           
          # vars.fault_type( tp, 0 )                  
          # vars.fault_type( tp2 )                    
          # vars.push_button( vars.flt_bt )     
          # time.sleep( 3 )
          
        elif caso == 11:  
          vars.push_button( vars.flt_bt )
          time.sleep( 0.2 )
          vars.push_button( vars.Opn_DSs[ "Opn_DS_LN2_Bus1_bt" ] ) 
          # vars.push_button( vars.DSs[ "Opn_DS_LA127_bt" ] )                    # Para el caso 'IntyMedio_0'
          
        elif caso == 12:  
          vars.push_button( vars.flt_bt )
          time.sleep( 0.2 )      
          vars.push_button( vars.Opn_DSs[ "Opn_DS_LN2_Bus2_bt" ] ) 
          # vars.push_button( vars.DSs[ "Opn_DS_LB127" ] )                       # Para el caso 'IntyMedio_0'           

        else: vars.push_button( vars.flt_bt )

        f_trip_time= vars.get_fltln_data( caso, vars.flt_loc[ pto_falla ] )
        
        goose_data_case= vars.get_goose_data( caso, f_trip_time )
        goose_data.append( goose_data_case )
        # time.sleep( 6 )                   
        
        print( f"----- Case { caso } executed successfully! ----    \n" )
        app.print_message( f"----- Case { caso } executed successfully! ----    \n" )  
        
        casefx.stop()    
        vars.checkpoint_sim()
        
        time.sleep( 1 )                           # CB Ready Supervision Time gap
          
      goose_data_df= pd.DataFrame( np.transpose( goose_data ), [ g for g in vars.goose_signals ] ).T
      print( f"\n -------- Goose_data_df: \n { goose_data_df } \n" )



      
      



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






# C110_3_TRIP= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|C110_3_TRIP" )       
# C110_3_TRIP_data= C110_3_TRIP.get_data()
# C110_3_TRIP_data_t= C110_3_TRIP.get_time_data()
    
# PROT_C110_A_Trip= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|PROT_C110_A_Trip" )       
# PROT_C110_A_Trip_data= PROT_C110_A_Trip.get_data()
# PROT_C110_A_Trip_data_t= PROT_C110_A_Trip.get_time_data()
    
# PROT_C110_B_Trip= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|PROT_C110_B_Trip" )       
# PROT_C110_B_Trip_data= PROT_C110_B_Trip.get_data()
# PROT_C110_B_Trip_data_t= PROT_C110_B_Trip.get_time_data()
    
# PROT_C110_C_Trip= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|PROT_C110_C_Trip" )       
# PROT_C110_C_Trip_data= PROT_C110_C_Trip.get_data()
# PROT_C110_C_Trip_data_t= PROT_C110_C_Trip.get_time_data()
    

# C010_3_TRIP= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|C010_3_TRIP" )       
# C010_3_TRIP_data= C010_3_TRIP.get_data()
# C010_3_TRIP_data_t= C010_3_TRIP.get_time_data()
    
# PROT_C010_A_Trip= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|PROT_C010_A_Trip" )       
# PROT_C010_A_Trip_data= PROT_C010_A_Trip.get_data()
# PROT_C010_A_Trip_data_t= PROT_C010_A_Trip.get_time_data()
    
# PROT_C010_B_Trip= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|PROT_C010_B_Trip" )       
# PROT_C010_B_Trip_data= PROT_C010_B_Trip.get_data()
# PROT_C010_B_Trip_data_t= PROT_C010_B_Trip.get_time_data()
    
# PROT_C010_C_Trip= casefx.get_signal( "Subsystem #1|GTNET|GTNET1|PROT_C010_C_Trip" )       
# PROT_C010_C_Trip_data= PROT_C010_C_Trip.get_data()
# PROT_C010_C_Trip_data_t= PROT_C010_C_Trip.get_time_data()