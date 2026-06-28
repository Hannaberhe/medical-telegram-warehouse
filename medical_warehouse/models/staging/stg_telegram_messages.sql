WITH raw AS (
    SELECT
        message_id,
        channel_name,
        message_date::timestamp AS message_date,
        message_text,
        views::int AS views,
        forwards::int AS forwards,
        has_media
    FROM raw.telegram_messages
    WHERE message_text IS NOT NULL AND message_text != ''
)
SELECT
    message_id, channel_name, message_date, message_text,
    LENGTH(message_text) AS message_length,
    views, forwards,
    CASE WHEN has_media = true THEN 1 ELSE 0 END AS has_image_flag
FROM raw
