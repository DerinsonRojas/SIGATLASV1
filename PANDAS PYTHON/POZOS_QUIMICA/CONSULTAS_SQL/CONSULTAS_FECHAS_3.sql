-- 1. Ver qué pozos tienen más actividad (muestras)
SELECT 
    id_pozo, 
    COUNT(*) as total_muestras,
    COUNT(DISTINCT fecha) as dias_diferentes
FROM 
    public.pozos_quimica
GROUP BY 
    id_pozo
ORDER BY 
    total_muestras DESC;