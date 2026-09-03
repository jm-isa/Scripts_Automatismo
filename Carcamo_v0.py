def execute_homologado_distancia(self, case_path: str, df_plan, rack_num: int,base_path: str, report_path: str):
  """Flujo estático para pruebas de Distancia (Protecciones de Relés)"""
  import time
  from rtds.constants import BUTTON, SLIDER, SWITCH

  # Filtramos por Enable == 1
  if "Enable" in df_plan.columns:
    df_plan["Resultado"] = "Pendiente"

  casos_a_ejecutar = df_plan[df_plan["Enable"] == 1] if "Enable" in df_plan.columns else df_plan

  self._log_write(f"Iniciando prueba homologada de Distancia. Total casos habilitados: {len(casos_a_ejecutar)}")

  try:
    with self.client.get_connection() as app:
      self._log_write("Conexión con RSCAD establecida. Abriendo caso...")
      case = app.open_case(case_path)

      try:
        case.settings.starting_rack = rack_num
        case.settings.set_plot_window_size(0.2)

        self._log_write("Compilando caso...")
        case.compile()

        # --- MAPEO ESTÁTICO DE OBJETOS ---
        self._log_write("Mapeando componentes fijos del caso D008...")
        flt_bt = case.get_object_by_name("FLT", BUTTON)
        flt_duration_sld = case.get_object_by_name("FLTDUR", SLIDER)

        line_length = {
          "LN1": case.get_object_by_name("Length_LN1", SLIDER),
          "LN3": case.get_object_by_name("Length_LN3", SLIDER),
          "LN4": case.get_object_by_name("Length_LN4", SLIDER)
        }

        resistance = {
          "LN1": case.get_object_by_name("Ron_LN1", SLIDER),
          "LN2": case.get_object_by_name("Ron_LN2", SLIDER),
          "LN3": case.get_object_by_name("Ron_LN3", SLIDER),
          "LN4": case.get_object_by_name("Ron_LN4", SLIDER)
        }

        flt_location = case.get_object_by_name('FLT_LOC', 'dial')

        # Fases
        switches = {
          "AG": case.get_object_by_name("AG", SWITCH),
          "BG": case.get_object_by_name("BG", SWITCH),
          "CG": case.get_object_by_name("CG", SWITCH),
          "AB": case.get_object_by_name("AB", SWITCH),
          "BC": case.get_object_by_name("BC", SWITCH),
          "CA": case.get_object_by_name("CA", SWITCH)
        }

        # Botones de Interruptores
        breakers = {
          "Opn3_BK_LN2_B1": case.get_object_by_name("Opn3_BK_LN2_B1", BUTTON),
          "Opn3_BK_LN2_B2": case.get_object_by_name("Opn3_BK_LN2_B2", BUTTON),
          "Cls3_BK_LN1_B1": case.get_object_by_name("Cls3_BK_LN1_B1", BUTTON),
          "Cls3_BK_LN1_B2": case.get_object_by_name("Cls3_BK_LN1_B2", BUTTON),
          "Cls3_BK_LN2_B1": case.get_object_by_name("Cls3_BK_LN2_B1", BUTTON),
          "Cls3_BK_LN2_B2": case.get_object_by_name("Cls3_BK_LN2_B2", BUTTON)
        }

        flt_loc_map = {"LN1": 1, "LN2": 2, "LN3": 3, "LN4": 4}

        # --- FUNCIÓN INTERNA DE CHECKPOINT ---
        def checkpoint_sim():
          self._log_write("--- CheckPoint: Reseteando variables ---")
          flt_bt.position = 0
          flt_duration_sld.value = 0
          flt_location.position = 1

          for ln in line_length.values(): ln.value = 50
          for res in resistance.values(): res.value = 1
          for sw in switches.values(): sw.position = 0

          # Cierre y apertura rápida de breakers de limpieza
          for bk_name in ["Cls3_BK_LN1_B1", "Cls3_BK_LN1_B2", "Cls3_BK_LN2_B1", "Cls3_BK_LN2_B2"]:
            breakers[bk_name].position = 1
            breakers[bk_name].position = 0
          time.sleep(1)

        # --- BUCLE PRINCIPAL DE EJECUCIÓN ---
        for index, row in casos_a_ejecutar.iterrows():
          # Usamos el Caso de la columna si existe, sino el índice del excel
          caso_num = row.get("Caso", index)


          self._log_write(f"--- Ejecutando Caso Homologado: {caso_num} ---")

          pto_falla = str(row["PtoFalla"]).strip()
          tipo_falla = str(row["TipoFalla"]).split('-')[0].strip()

          # Configurar Resistencia y Distancia
          if pto_falla in resistance:
            resistance[pto_falla].value = float(row["RFalla"])

          dist = int(row["DistPcnt"])
          if caso_num in [11, 12]:
            line_length["LN1"].value = dist
          elif pto_falla in line_length:
            line_length[pto_falla].value = dist

          # Configurar Duración y Ubicación
          tf = float(row["TFalla"])
          flt_duration_sld.value = tf
          if pto_falla in flt_loc_map:
            flt_location.position = flt_loc_map[pto_falla]

          # Lógica de Fases Especial
          if caso_num == 10:
            switches["AG"].position = 1
          else:
            # Mapeo general de falla
            if "A" in tipo_falla and "B" not in tipo_falla and "C" not in tipo_falla: switches["AG"].position = 1
            if "B" in tipo_falla and "A" not in tipo_falla and "C" not in tipo_falla: switches["BG"].position = 1
            if "C" in tipo_falla and "A" not in tipo_falla and "B" not in tipo_falla: switches["CG"].position = 1
            if "AB" in tipo_falla: switches["AG"].position, switches["BG"].position = 1, 1
            if "AC" in tipo_falla or "CA" in tipo_falla: switches["AG"].position, switches["CG"].position = 1, 1
            if "BC" in tipo_falla: switches["BG"].position, switches["CG"].position = 1, 1
            if "ABC" in tipo_falla: switches["AG"].position, switches["BG"].position, switches["CG"].position = 1, 1, 1

          # Ejecutar Simulación
          case.compile() # El script original compila dentro del ciclo.
          case.run()
          time.sleep(3)

          # Disparo
          flt_bt.position = 1
          flt_bt.position = 0

          # Comportamientos Evolutivos y de Apertura (Casos 10, 11, 12)
          if caso_num == 10:
            time.sleep(tf)
            switches["AG"].position = 0
            switches["BG"].position = 1
            flt_bt.position = 1
            flt_bt.position = 0
            time.sleep(3)
          elif caso_num == 11:
            time.sleep(0.2)
            breakers["Opn3_BK_LN2_B1"].position = 1
            breakers["Opn3_BK_LN2_B1"].position = 0
          elif caso_num == 12:
            time.sleep(0.2)
            breakers["Opn3_BK_LN2_B2"].position = 1
            breakers["Opn3_BK_LN2_B2"].position = 0

          time.sleep(3)
          self._log_write(f"Caso {caso_num} ejecutado exitosamente.")

          case.stop()
          checkpoint_sim()
          time.sleep(2)

      finally:
        self._log_write("Cerrando caso en RSCAD y liberando recursos...")
        case.close()

  except Exception as e:
    self._log_write(f"Error crítico en la ejecución: {e}")
    raise  # Relanzamos para que la API sepa que hubo error

  finally:
    # GUARDAMOS EL EXCEL DE RESULTADOS
    self._log_write(f"Guardando reporte final en: {report_path}")
    df_plan.to_excel(report_path, index=False)