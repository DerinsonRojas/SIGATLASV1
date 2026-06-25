-- Queremos ver qué formatos existen en la tabla y cuántos registros hay de cada uno
SELECT 
    fecha, 
    COUNT(*) as frecuencia
FROM 
    public.pozos_quimica
GROUP BY 
    fecha
ORDER BY 
    frecuencia DESC;