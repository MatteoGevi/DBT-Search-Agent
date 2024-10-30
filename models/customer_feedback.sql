-- models/customer_feedback.sql

SELECT
    feedback_id,
    customer_id,
    feedback_text,
    feedback_date
FROM
    raw.customer_feedback_data