"""
MÓDULO: Pipeline de Extracción, Limpieza y Carga (ETL) - Datos de Quimica de Pozos
PROYECTO: Prueba de Concepto - Tesis de Grado
AUTOR: DERINSON ROJAS
DESCRIPCIÓN: 
    (Script de ETL y conección a BBDD PostgresSQL funcional) 
    Este script automatiza la ingesta y aplica las reglas de validación técnica
    identificadas en la auditoría de datos (filtros de diámetros, normalización 
    de indicadores booleanos y preservación de códigos de estatatus de las propiedades
    químicas de los pozos de la BBDD).
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# ==========================================
# 1. EXTRACCIÓN (Ingesta de datos crudos)
# ==========================================
print(">> Iniciando extracción de datos...")
df = pd.read_csv(
    "pozosQuimica.txt", 
    sep=";", 
    encoding="Latin-1",
    na_values=["", " "],       
    skipinitialspace=True,
    quotechar='"'      
)

# ==========================================
# 2. TRANSFORMACIÓN (Reglas de Ingeniería de Datos)
# ==========================================


# 2.1. Diccionario de Renombramiento Formal (Estandarización de Esquema)
df.columns = df.columns.str.lower()

diccionario_nombres = {
    'iden': 'id_pozo'
}
df = df.rename(columns=diccionario_nombres)

# 2.2. Limpieza de columnas numéricas (Reemplazar ',' por '.'), Cambio a valor númerico en cada columna donde corresponda
# Columnas que contienen concentraciones (ejemplo: 'calcio', 'nitratos', etc.)
columnas_numericas = ['temp','ph','indice','conduc','alc','dtotal','tsd','ras','cl','so4',
                      'f','no2','no3','sio2','hco3','co3','fe','mn','b','duca','ca','mg','na','k',
                      'cu','zn','pb','po4'] # Columnas con valores númericos

for col in columnas_numericas:
    # Convertimos a string por si hay valores nulos o formatos mixtos
    df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
    # Convertimos a numérico, forzando error a NaN para registros corruptos
    df[col] = pd.to_numeric(df[col], errors='coerce')

#2.3. Estandarización de Fechas (ACT_QUIMI)
# act_master: El significado exacto es desconocido. 
#             Se sospecha que podría ser fecha de perforación o última visita.
#             Se conserva el nombre original para preservar la trazabilidad 
#             con el sistema de origen hasta que se confirme su semántica.
#Transformación
df['act_quimi'] = pd.to_datetime(df['act_quimi'], dayfirst=True, errors='coerce').dt.normalize()

## Comprobación de integridad
total_nulos = df['act_quimi'].isna().sum()
if total_nulos > 0:
    print(f">>Atención: {total_nulos} valores en 'act_quimi' no pudieron convertirse a fecha y se han convertido en NaT.")

#2.4. Estandarización para la columna fecha
#La nueva columna fecha tiene un formato original tipo texto con celdas con formatos "----"
#para marcar valores faltantes, se trabaja a continuación para igualar al formato correcto para fechas

'''# 2.5. Control de Duplicados en la Clave Primaria

print(f">> Registros antes de eliminar duplicados de ID: {len(df)}")

# Conservamos la primera aparición del ID de pozo y eliminamos las réplicas
df = df.drop_duplicates(subset=['id_pozo'], keep='first')

print(f">> Registros tras eliminar duplicados de ID: {len(df)}")
'''
# ==========================================
# 3. CARGA (Persistencia y Restricciones SQL)
# ==========================================
print(">> Exportando archivo plano CSV...")
df.to_csv("24062026_DATOS_LIMPIOS_POZOS_QUIMICA.csv", index=False, encoding="utf-8", sep=";")     

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
df.to_sql(name="pozos_quimica", con=engine, if_exists="append", index=False)


#Lectura de las fechas limpias por si es necesario algún calculo extra con valores del campo fecha correctos
query = "SELECT * FROM v_fechas_analitica WHERE estado_fecha = 'VALIDA'"
df_limpio = pd.read_sql(query, engine)
'''
# Asignación formal de la PRIMARY KEY en PostgreSQL
# Usamos engine.begin() para que maneje el COMMIT automáticamente sin fallar por versión
with engine.begin() as con:
    print(">> Asignando clave primaria 'id_pozo' en la base de datos...")
    con.execute(text("ALTER TABLE public.pozos_master ADD PRIMARY KEY (id_pozo);"))
'''
print(">> Pipeline Fase 2 unificado y ejecutado con éxito total.")