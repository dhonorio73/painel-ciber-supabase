-- Consultas de diagnóstico, somente leitura. Revise os formatos antes de converter datas.
SELECT data_hora, count(*) AS quantidade
FROM public.historico_pesquisas
GROUP BY data_hora ORDER BY quantidade DESC;

SELECT count(*) AS total,
       count(*) FILTER (WHERE data_hora IS NULL OR trim(data_hora) = '') AS datas_ausentes,
       count(*) FILTER (WHERE departamento IS NULL OR trim(departamento) = '') AS departamentos_ausentes
FROM public.historico_pesquisas;

SELECT departamento, count(*) AS total
FROM public.historico_pesquisas
GROUP BY departamento ORDER BY total DESC;
