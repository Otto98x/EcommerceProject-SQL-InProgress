-- Rough 

--select column_name, data_type
--from information_schema.columns
--where table_schema = 'public' and table_name = 'orders';
--
---- Write a query that:
---- 1. Joins orders and order_items
---- 2. Calculates previous order date using LAG
---- 3. Calculates days between orders
---- 4. Finds the average days between orders for each customer
--
---- Order Value Calculation
--select 
--	order_id,
--	order_date,
--	SUM(oi.quantity * oi.unit_price) as order_value
--from orders o
--left join order_items oi 
--	using (order_id)
--group by 1,2
--
---- Customer spendig metrics and frequency
--
--select 
--	o.customer_id,
--	COUNT(distinct o.order_id) as order_count,
--	SUM(oi.quantity * oi.unit_price) as order_value,
--	AVG(oi.quantity * oi.unit_price) as avg_order_value
--from orders o
--left join order_items oi USING(order_id)
--group by 1;
--
---- Prev order date for Purchase frequency analysis
--select 
--	customer_id,
--	order_date,
--	LAG(order_date) OVER(partition by customer_id order by order_date) as prev_order_date
--from orders o;
--
---- Calcualting gap between orders for Purchase Frequency Analysis
--
--select 
--	customer_id,
--	order_date,
--	prev_order_date,
--	DATE_PART('days', AGE(order_date, prev_order_date)) as days_between_orders
--from (
--	select 
--		customer_id,
--		order_date,
--		LAG(order_date) OVER(partition by customer_id order by order_date) as prev_order_date
--	from orders 
--) subquery
--where prev_order_date is not null;
--
---- Diving customer into quartiles by order spending
--select
--	customer_id,
--	order_value,
--	NTILE(4) OVER(order by order_value) as spend_quartile
--from (
--	select 
--		o.customer_id,
--		SUM(oi.quantity * oi.unit_price) as order_value
--	from orders o
--	left join order_items oi USING(order_id)
--	group by 1
--) customer_spend;

-------------
-- Final Query

-- Calculating Order Values and Tracking Purchase timings

with customer_purchases as(
	select 	
		o.customer_id, 
		o.order_date,
		SUM(od.unit_price * od.quantity) as order_value,
		LAG(o.order_date) over (partition by customer_id order by order_date) as prev_order_date
	from orders o
	left join order_items od USING(order_id)
	group by 1, 2
), 
-- customer spending behavior
purchase_metrics as ( 
	select 
		customer_id,
		AVG(date_part('day', AGE(order_date, prev_order_date))) as avg_days_between_orders,
		SUM(order_value) as total_spend,
		COUNT(customer_id) as total_orders,
		AVG(order_value) as avg_order_value
	from customer_purchases
	group by 1
 ),
 -- grouping by quartiles
 quartiles as (
 	select 
 	*,
 	NTILE(4) OVER(order by total_spend) as spend_quartile
 	from purchase_metrics
 )
-- bringing everything together
select
	spend_quartile,
	ROUND(AVG(avg_days_between_orders)) as avg_purchase_frequency,
	ROUND(AVG(total_spend), 2) as avg_total_spend, 
	ROUND(AVG(total_orders)) as avg_orders
from quartiles
group by 1
order by 1;