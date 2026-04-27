from conciliacion import (
    cargar_datos,
    cruce_exacto,
    obtener_pendientes,
    cruce_fuzzy,
    actualizar_conciliacion,
    exportar_excel
)

# ── Rutas ────────────────────────────────────────────────────────────────────
RUTA_MAYOR         = 'C:\\Users\\HP\\Documents\\1.Fabricio Coque\\17.Portfolio Web\\Conciliacion_Nacional_PYME\\01_Datos_Entrada\\mayor_contable.xlsx'
RUTA_ESTADO_CUENTA = 'C:\\Users\\HP\\Documents\\1.Fabricio Coque\\17.Portfolio Web\\Conciliacion_Nacional_PYME\\01_Datos_Entrada\\estado_cuenta.xlsx'
RUTA_OUTPUT        = 'C:\\Users\\HP\\Documents\\1.Fabricio Coque\\17.Portfolio Web\\Conciliacion_Nacional_PYME\\02_Resultados\\conciliacion_resultado.xlsx'


# ── Ejecutar ─────────────────────────────────────────────────────────────────
df_mayor, df_bancos = cargar_datos(RUTA_MAYOR, RUTA_ESTADO_CUENTA)

df_conc_mayor, df_conc_banco = cruce_exacto(df_mayor, df_bancos)

df_partidas_pendientes, df_depositos_sobrantes = obtener_pendientes(df_conc_mayor, df_conc_banco)

df_fuzzy_matches = cruce_fuzzy(df_partidas_pendientes, df_depositos_sobrantes, umbral=80)

df_conc_mayor, df_conc_banco = actualizar_conciliacion(df_conc_mayor, df_conc_banco, df_fuzzy_matches)

df_partidas_pendientes, df_depositos_sobrantes = obtener_pendientes(df_conc_mayor, df_conc_banco)

exportar_excel(df_conc_mayor, df_conc_banco, df_partidas_pendientes,
               df_depositos_sobrantes, df_fuzzy_matches, RUTA_OUTPUT)
