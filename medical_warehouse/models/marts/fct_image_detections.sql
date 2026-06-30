WITH yolo_results AS (
    SELECT
        message_id,
        channel_name,
        detected_class,
        confidence_score,
        CASE
            WHEN detected_class IN ('bottle', 'cup', 'bowl') THEN 'product_display'
            WHEN detected_class = 'person' THEN 'promotional'
            ELSE 'other'
        END AS image_category
    FROM raw.yolo_detections
)

SELECT
    f.message_id,
    f.channel_key,
    f.date_key,
    y.detected_class,
    y.confidence_score,
    y.image_category
FROM {{ ref('fct_messages') }} f
JOIN yolo_results y ON f.message_id = y.message_id
