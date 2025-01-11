--RevenueTracking

--Rough
--Calculating Daily Revenue
--
--select 
--	date_trunc('day', order_date) as date,
--	SUM(oi.unit_price * oi.quantity)
--from orders o 
--left join order_items oi using (order_id)
--group by 1;


--Final Query
-- Adding unique customer count to daily revenue + changing scaffolding to CTE + -- calculating 7 & 30d day moving average
WITH daily_revenue AS (
    SELECT 
        DATE_TRUNC('day', order_date) AS date,
        SUM(oi.unit_price * oi.quantity) AS revenue,
        COUNT(DISTINCT customer_id) AS customers
    FROM orders o
    LEFT JOIN order_items oi USING (order_id)
    GROUP BY 1
)
SELECT 
    date,
    revenue,
    AVG(revenue) OVER(ORDER BY date ROWS BETWEEN 7 PRECEDING AND CURRENT ROW) AS moving_avg_7d,
    AVG(revenue) OVER(ORDER BY date ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) AS moving_avg_30d
FROM daily_revenue;