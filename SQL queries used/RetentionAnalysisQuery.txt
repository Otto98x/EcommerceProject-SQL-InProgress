-- Rough

-- See all column names
--select column_name, data_type
--from information_schema.columns
--where table_schema = 'public'
--and table_name = 'orders';

-- Get all customer ID and signup Dates
select customer_id, signup_date
from customers;

-- See Original Signup Date and truncated month
select 
	signup_date,
	DATE_TRUNC('month',signup_date) as cohort_month
from customers;

--Matching customers with their orders
select
	c.customer_id,
	c.signup_date,
	o.order_id 
from customers c
left join orders o USING (customer_id);

-- Joining cohort_month and order month in CTE
--with cohort_base as (
--	select 
--		customer_id,
--		date_trunc('month', signup_date) as cohort_month,
--		date_trunc('month', order_date) as order_month
--	from customers c 
--	left join orders o USING(customer_id)
--)	

-- -- Customer count by cohort with cohort_base CTE
--select 
--	cohort_month,
--	COUNT(DISTINCT customer_id) as customer_count
--from cohort_base
--group by cohort_month;

-- Practicing window function - adding number of months since signup + active customers
--select 
--	cohort_month,
--	order_month,
--	COUNT(DISTINCT customer_id) as active_customer
--	row_number () over(PARTITION by cohort_month order by cohort_month ) - 1 as month_number
--from cohort_base;


-- Final Query
-- Joining cohort_month and order month in CTE
with cohort_base as (
	select 
		customer_id,
		date_trunc('month', signup_date) as cohort_month,
		date_trunc('month', order_date) as order_month
	from customers c 
	left join orders o USING(customer_id)
),	
-- Calculating cohort size
cohort_size as (
	select
		COUNT(distinct customer_id) as registered_count,
		cohort_month
	from cohort_base
	group by cohort_month
),
month_active_customer as (
	select 
		cohort_month,
		order_month,
		COUNT(DISTINCT customer_id) as active_customer,
		row_number () over(PARTITION by cohort_month order by order_month) - 1 as month_number
	from cohort_base
	group by 1,2
)
-- retention rate calc
select 
	c.cohort_month,
	mac.month_number,
	ROUND(100.0 * mac.active_customer / c.registered_count,2) as rentention_rate
from cohort_size c
left join month_active_customer mac using (cohort_month);
