SELECT 
    CASE 
        WHEN indice < -3.0 THEN '1. Altamente Corrosivo (Peligro Tuberías)'
        WHEN indice BETWEEN -3.0 AND -0.5 THEN '2. Moderadamente Corrosivo'
        WHEN indice BETWEEN -0.5 AND 0.5 THEN '3. Neutro / En Equilibrio'
        WHEN indice BETWEEN 0.5 AND 3.0 THEN '4. Moderadamente Incrustante'
        WHEN indice BETWEEN 3.0 AND 5.0 THEN '5. Altamente Incrustante (Peligro Obstrucción)'
        WHEN indice > 5.0 THEN '6. Extremo / Sospechoso (> 5)'
        ELSE '7. Sin Dato (NULL)'
    END AS clasificacion_langelier,
    COUNT(*) AS cantidad_pozos,
    ROUND((COUNT(*)::NUMERIC / SUM(COUNT(*)) OVER ()) * 100, 2) AS porcentaje
FROM public.pozos_quimica
GROUP BY 1
ORDER BY clasificacion_langelier;