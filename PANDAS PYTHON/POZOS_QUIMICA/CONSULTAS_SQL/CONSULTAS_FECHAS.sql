SELECT id_pozo,
COUNT (*) AS cantidad
FROM public.pozos_quimica
GROUP BY id_pozo
ORDER BY cantidad DESC;
