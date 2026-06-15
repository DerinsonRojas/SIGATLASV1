# 🚰 SIGATLASV1: ETL & Data Migration for Hydraulic Infrastructure

## 📌 Descripción del Proyecto
Este proyecto consiste en el desarrollo de un pipeline de ingeniería de datos para la **limpieza, normalización y migración** de un sistema de información histórico de infraestructura hidráulica (específicamente registros de pozos profundos de agua subterránea). 

El objetivo principal es transformar una base de datos heredada en formato **Microsoft Access**, resolver inconsistencias críticas en los registros y migrar la estructura optimizada hacia un sistema de gestión relacional robusto en **PostgreSQL** (con proyección a soporte espacial mediante **PostGIS**).

## 🚀 Características Técnicas
* **Extracción y Limpieza (ETL):** Procesamiento de tablas mediante **Python y Pandas** para la eliminación de duplicados, normalización de tipos de datos y manejo de registros nulos.
* **Estructuración Geográfica:** Limpieza y estandarización de coordenadas geográficas/proyecciones para asegurar la futura integridad espacial de los puntos de captación.
* **Migración Relacional:** Diseño del nuevo esquema de datos optimizado para su inserción eficiente en PostgreSQL.

## 🛠️ Stack Tecnológico
* **Python 3.x**
* **Pandas:** Para la manipulación y análisis de las estructuras de datos.
* **Microsoft Access (Origen) ➡️ PostgreSQL / PostGIS (Destino)**

## 📂 Estructura del Repositorio
```text
SIGATLASV1/
├── BBDD SIGATLAS/
├── BITACORA/
├── DATOS LIMPIOS/
├── PANDAS PYTHON/
├── SCRIPS FINALES/
├── TABLAS PROVENIENTES DE ACCES A TXT/
└── README.md


Estado del Proyecto
Actualmente el proyecto se encuentra en fase de desarrollo activo (Work in Progress), enfocado en la fase de transformación de datos (T) y diseño del esquema de destino en la base de datos.