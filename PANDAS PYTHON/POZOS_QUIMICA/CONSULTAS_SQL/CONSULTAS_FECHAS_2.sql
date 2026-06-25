-- 2. Confirmar si un mismo pozo tiene múltiples muestras en la misma fecha
-- (Esto te dirá si hay datos duplicados reales o si son mediciones distintas el mismo día)
SELECT 
    id_pozo, 
    fecha, 
    COUNT(*) as muestras_el_mismo_dia
FROM 
    public.pozos_quimica
GROUP BY 
    id_pozo, fecha
HAVING COUNT(*) > 1
ORDER BY muestras_el_mismo_dia DESC;