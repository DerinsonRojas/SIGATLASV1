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

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# ==========================================
# 1. EXTRACCIÓN (Ingesta de datos crudos)
# ==========================================
print(">> Iniciando extracción de datos...")
df = pd.read_csv(
    "pozosNivel.txt", 
    sep=";", 
    encoding="Latin-1",
    na_values=["", " "],       
    skipinitialspace=True      
)
