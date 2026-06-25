CREATE OR REPLACE VIEW v_fechas_analitica AS
SELECT 
    id_pozo,
    CASE 
        WHEN fecha ~ '^[0-3][1-9][0-1][0-2][0-9]{2}$' 
             AND SUBSTRING(fecha, 3, 2) BETWEEN '01' AND '12'
        THEN 
            CASE 
                WHEN EXTRACT(YEAR FROM TO_DATE(fecha, 'DDMMYY')) > 2026 
                THEN TO_DATE(fecha, 'DDMMYY') - INTERVAL '100 years' 
                ELSE TO_DATE(fecha, 'DDMMYY') 
            END
        ELSE NULL 
    END AS fecha_analisis,
    CASE 
        WHEN fecha ~ '^[0-3][1-9][0-1][0-2][0-9]{2}$' 
             AND SUBSTRING(fecha, 3, 2) BETWEEN '01' AND '12'
        THEN 'VALIDA'
        ELSE 'INCERTIDUMBRE'
    END AS estado_fecha
FROM public.pozos_quimica;