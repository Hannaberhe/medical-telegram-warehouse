WITH dates AS (
    SELECT generate_series('2024-01-01'::date, '2026-12-31'::date, '1 day'::interval) AS full_date
)
SELECT TO_CHAR(full_date, 'YYYYMMDD')::int AS date_key, full_date,
       EXTRACT(DOW FROM full_date) AS day_of_week,
       EXTRACT(WEEK FROM full_date) AS week_of_year,
       EXTRACT(MONTH FROM full_date) AS month,
       EXTRACT(YEAR FROM full_date) AS year,
       CASE WHEN EXTRACT(DOW FROM full_date) IN (0,6) THEN true ELSE false END AS is_weekend
FROM dates
