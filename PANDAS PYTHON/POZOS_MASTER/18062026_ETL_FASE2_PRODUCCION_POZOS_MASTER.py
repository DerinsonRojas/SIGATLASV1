"""
MÓDULO: Pipeline de Extracción, Limpieza y Carga (ETL) - Datos de Pozos
PROYECTO: Prueba de Concepto - Tesis de Grado
AUTOR: DERINSON ROJAS
DESCRIPCIÓN: 
    Fase 2 - Limpieza Avanzada y Control de Calidad.
    Este script automatiza la ingesta y aplica las reglas de validación técnica
    identificadas en la auditoría de datos (filtros de diámetros, normalización 
    de indicadores booleanos y preservación de códigos de estatus históricos).
"""

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# ==========================================
# 1. EXTRACCIÓN (Ingesta de datos crudos)
# ==========================================
print(">> Iniciando extracción de datos...")
df = pd.read_csv(
    "pozosMaster.txt", 
    sep=";", 
    encoding="Latin-1",
    na_values=["", " "],       
    skipinitialspace=True      
)

# ==========================================
# 2. TRANSFORMACIÓN (Reglas de Ingeniería de Datos)
# ==========================================
print(">> Ejecutando reglas de transformación y calidad...")

# 2.1. Diccionario de Renombramiento Formal (Estandarización de Esquema)
df.columns = df.columns.str.lower()

diccionario_nombres = {
    'iden': 'id_pozo',
    'diam1': 'diametro_superior_in',
    'diam2': 'diametro_inferior_in',
    'pbombeo': 'ind_bombeo',
    'reg': 'ind_registro',
    'epozo': 'cod_estatus_pozo',
    'nivel': 'nivel_estatico_m',     
    'nd': 'nivel_dinamico_m',
    'prop': 'propietario',           
    'lat': 'latitud',                 
    'lon': 'longitud',
    'gasto':'gasto_l_s',
    'perf':'prof_perforacion_m',
    'norte':'norte_m',
    'este':'este_m',
    'cota':'altitud_msnm',
    'entu':'prof_entubado_m'                 
}
df = df.rename(columns=diccionario_nombres)

# 2.2. Conversión Forzada de Columnas Numéricas Fidedignas
# ¡PRIMERO PASAMOS A NÚMERO! Así limpiamos cualquier texto oculto en los diámetros.
columnas_numericas = [
    'latitud', 'longitud', 'prof_perforacion_m', 'gasto_l_s', 'altitud_msnm', 
    'prof_entubado_m', 'nivel_estatico_m', 'nivel_dinamico_m', 'norte_m', 'este_m',
    'diametro_superior_in','diametro_inferior_in',
]
for col in columnas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 2.3. Control de Calidad Técnico para Diámetros (Umbral de 30" y Regla Telescópica)

if 'diametro_superior_in' in df.columns:
    df.loc[df['diametro_superior_in'] > 30, 'diametro_superior_in'] = pd.NA

if 'diametro_inferior_in' in df.columns:
    df.loc[df['diametro_inferior_in'] > 30, 'diametro_inferior_in'] = pd.NA

# Regla Telescópica segura: Solo se aplica si AMBOS diámetros existen y el superior es menor al inferior
if 'diametro_superior_in' in df.columns and 'diametro_inferior_in' in df.columns:
    asimetria_diametros = (
        df['diametro_superior_in'].notna() & 
        df['diametro_inferior_in'].notna() & 
        (df['diametro_superior_in'] < df['diametro_inferior_in'])
    )
    df.loc[asimetria_diametros, ['diametro_superior_in', 'diametro_inferior_in']] = pd.NA


# 2.4. Normalización Booleana Fidedigna para 'ind_bombeo' (Antiguo PBOMBEO)
mapeo_bombeo = {'SI': True, 'X': True, 'NO': False}
df['ind_bombeo'] = df['ind_bombeo'].map(mapeo_bombeo).astype('object')

# 2.5. Normalización Booleana Fidedigna para 'ind_registro' (Antiguo REG)
mapeo_registro = {'SI': True, 'S': True, 'X': True, 'NO': False, '0': False}
df['ind_registro'] = df['ind_registro'].map(mapeo_registro).astype('object')

# 2.6. Preservación Estricta de Códigos Informativos 'cod_estatus_pozo' (Antiguo EPOZO)
if 'cod_estatus_pozo' in df.columns:
    df['cod_estatus_pozo'] = df['cod_estatus_pozo'].str.upper()


# 2.7. Control de Duplicados en la Clave Primaria

print(f">> Registros antes de eliminar duplicados de ID: {len(df)}")

# Conservamos la primera aparición del ID de pozo y eliminamos las réplicas
df = df.drop_duplicates(subset=['id_pozo'], keep='first')

print(f">> Registros tras eliminar duplicados de ID: {len(df)}")

# 2.8. Presevación de columnas desconocidas const y fneiv como string para preservar la data legacy

columnas_legacy = ['feniv','const']
# Forzamos la conversión a 'string' (el tipo de dato nativo de texto en Pandas)
# Si la versión de pandas es algo antigua, usar 'object' en lugar de 'string'
df[columnas_legacy] = df[columnas_legacy].astype('string')

#2.9. Estandarización de Fechas (ACT_MASTER)
# act_master: El significado exacto es desconocido. 
#             Se sospecha que podría ser fecha de perforación o última visita.
#             Se conserva el nombre original para preservar la trazabilidad 
#             con el sistema de origen hasta que se confirme su semántica.
df['act_master'] = pd.to_datetime(df['act_master'], dayfirst=True, errors='coerce').dt.normalize()
if 'feniv' in df.columns:
    df['feniv'] = pd.to_datetime(df['feniv'], dayfirst=True, errors='coerce').dt.normalize()


# ==========================================
# 3. CARGA (Persistencia y Restricciones SQL)
# ==========================================
print(">> Exportando archivo plano CSV...")
df.to_csv("22062026_DATOS_LIMPIOS_POZOS_MASTER.csv", index=False, encoding="utf-8", sep=";")     

print(">> Conectando con PostgreSQL para la carga...")
load_dotenv()
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

URL_CONEXION = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
engine = create_engine(URL_CONEXION)

# Inyección inicial en base de datos
df.to_sql(name="pozos_master", con=engine, if_exists="replace", index=False)

# Asignación formal de la PRIMARY KEY en PostgreSQL
# Usamos engine.begin() para que maneje el COMMIT automáticamente sin fallar por versión
with engine.begin() as con:
    print(">> Asignando clave primaria 'id_pozo' en la base de datos...")
    con.execute(text("ALTER TABLE public.pozos_master ADD PRIMARY KEY (id_pozo);"))

print(">> Pipeline Fase 2 unificado y ejecutado con éxito total.")