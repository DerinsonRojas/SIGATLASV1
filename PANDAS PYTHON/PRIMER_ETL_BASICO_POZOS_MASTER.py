import pandas as pd
import sqlite3

# Leer el archivo
df = pd.read_csv("pozosMaster.txt", sep=";", 
                 encoding="Latin-1",
                 na_values=["", " "], # Clave: trata espacios vacíos como NaN,
                 skipinitialspace=True) # Opcional: elimina espacios extra alrededor de los valores)

# Mostrar las primeras 5 filas en la consola
#print(df.head())

#Mostrar la info del DATAFRAME
#print(df.info())

#Estas instrucciones transforman los campos vacios de las columnas numericas a NULL, para que pueda quedar flotante la columna
columnas_numericas = ['LAT', 'LON','CONST','PERF','FNIV','GASTO','COTA','ENTU', 'NIVEL', 'ND', 'DIAM1', 'DIAM2', 'NORTE', 'ESTE']
for col in columnas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

        
# Verificar el resultado
print(df.dtypes)


# Convertir la columna a datetime
# dayfirst=True es crucial para formatos DD/MM/YYYY
df['ACT_MASTER'] = pd.to_datetime(df['ACT_MASTER'], dayfirst=True, errors='coerce')

# Mantener como datetime64 (Recomendado para SQL)
# Esto pone la hora en 00:00:00 internamente, pero SQL lo maneja bien como DATE
df['ACT_MASTER'] = df['ACT_MASTER'].dt.normalize()

#print(df['ACT_MASTER'].dtype) 
# Debe decir: datetime64[ns]

#print(df['ACT_MASTER'].head())
# Debe mostrar: 1994-01-18 (sin la hora visible o con 00:00:00 estandarizado)   

# Guardar como CSV sin índices y con codificación UTF-8
df.to_csv("datos_limpios.csv", index=False, encoding="utf-8", sep=";")   

# Crear conexión y guardar directamente
df.to_sql("mi_tabla_limpia", con=sqlite3.connect("mis_datos.db"), if_exists="replace", index=False)   