-- models/sales.sql

SELECT
    sale_id,
    product_id,
    quantity_sold,
    sale_date
FROM
    raw.sales_records