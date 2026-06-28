WITH stats AS (
    SELECT channel_name, MIN(message_date) AS first_post,
           MAX(message_date) AS last_post, COUNT(*) AS total_posts,
           ROUND(AVG(views), 2) AS avg_views
    FROM {{ ref('stg_telegram_messages') }} GROUP BY channel_name
)
SELECT ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_key,
       channel_name,
       CASE WHEN channel_name LIKE '%pharma%' THEN 'Pharmaceutical'
            WHEN channel_name LIKE '%cosmetic%' OR channel_name LIKE '%lobelia%' THEN 'Cosmetics'
            ELSE 'Medical' END AS channel_type,
       first_post, last_post, total_posts, avg_views
FROM stats
