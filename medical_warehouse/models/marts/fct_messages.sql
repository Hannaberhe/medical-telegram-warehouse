WITH messages AS (
    SELECT
        m.message_id,
        d.date_key,
        c.channel_key,
        m.message_text,
        m.message_length,
        m.views,
        m.forwards,
        m.has_image_flag
    FROM {{ ref('stg_telegram_messages') }} m
    LEFT JOIN {{ ref('dim_dates') }} d
        ON DATE(m.message_date) = d.full_date
    LEFT JOIN {{ ref('dim_channels') }} c
        ON m.channel_name = c.channel_name
)

SELECT * FROM messages
