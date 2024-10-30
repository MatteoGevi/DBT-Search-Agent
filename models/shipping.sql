-- models/shipping.sql

SELECT
    shipping_id,
    order_id,
    shipping_date,
    delivery_date
FROM
    raw.shipping_info