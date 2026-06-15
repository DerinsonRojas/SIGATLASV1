"""
MÓDULO: Pipeline de Extracción, Limpieza y Carga (ETL) - Datos de Pozos
PROYECTO: Prueba de Concepto - Tesis de Grado
AUTOR: DERINSON ROJAS
DESCRIPCIÓN: 
    Este script automatiza la ingesta de datos crudos de pozos provenientes de 
    una exportación de Microsoft Access (.txt). Realiza la normalización de 
    valores nulos, conversión forzada de tipos de datos numéricos, estandarización 
    de fechas (formatos DD/MM/YYYY) y exporta los datos limpios tanto a un archivo 
    plano estandarizado (CSV) como a una base de datos relacional local (SQLite).
"""

import pandas as pd
import sqlite3

# ==========================================
# 1. EXTRACCIÓN (Ingesta de datos crudos)
# ==========================================

# Se lee el archivo manejando la codificación de Windows (Latin-1) 
# y estandarizando los espacios en blanco como valores NaN desde el inicio.
df = pd.read_csv(
    "pozosMaster.txt", 
    sep=";", 
    encoding="Latin-1",
    na_values=["", " "],       # Trata espacios vacíos como nulos (NaN)
    skipinitialspace=True      # Elimina espacios en blanco accidentales en los bordes
)


# ==========================================
# 2. TRANSFORMACIÓN (Limpieza y Tipado de Datos)
# ==========================================

# 2.1. Conversión Forzada de Columnas Numéricas
# Al exportar de Access, los valores faltantes o caracteres extraños rompen el tipo numérico.
# 'errors=coerce' transforma cualquier texto no numérico o vacío en NaN (NULL), 
# permitiendo que Pandas reconozca la columna como tipo flotante (Float64).
columnas_numericas = [
    'LAT', 'LON', 'CONST', 'PERF', 'FNIV', 'GASTO', 'COTA', 
    'ENTU', 'NIVEL', 'ND', 'DIAM1', 'DIAM2', 'NORTE', 'ESTE'
]

for col in columnas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 2.2. Estandarización de Fechas
# Se parsea el texto a objeto datetime reconociendo el formato latino (Día primero).
# 'errors=coerce' invalida fechas mal formateadas o corruptas convirtiéndolas en NaT (Not a Time).
df['ACT_MASTER'] = pd.to_datetime(df['ACT_MASTER'], dayfirst=True, errors='coerce')

# Se normaliza la fecha para eliminar el componente de hora (truncar a las 00:00:00)
# Esto garantiza compatibilidad óptima con los tipos de datos DATE de los motores SQL.
df['ACT_MASTER'] = df['ACT_MASTER'].dt.normalize()


# ==========================================
# 3. CARGA (Persistencia de Datos)
# ==========================================

# 3.1. Exportación a Formato Plano Estandarizado (CSV)
# Se guarda en UTF-8 (estándar moderno) sin incluir el índice autogenerado de Pandas.
df.to_csv("12062026_DATOS_LIMPIOS_POZOS_MASTER.csv", index=False, encoding="utf-8", sep=";")   

# 3.2. Carga en Base de Datos Relacional (SQLite)
# Se crea un archivo de base de datos local 'mis_datos.db' y se almacena la información.
# Si la tabla ya existe, se reemplaza ('replace') para evitar duplicidad en ejecuciones sucesivas.
with sqlite3.connect("mis_datos.db") as conexion:
    df.to_sql(
        name="POZOS_MASTER", 
        con=conexion, 
        if_exists="replace", 
        index=False
    )

print(">> Pipeline ejecutado con éxito. Datos limpios y guardados en CSV y SQLite.")