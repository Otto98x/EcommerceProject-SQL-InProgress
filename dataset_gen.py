import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Generate customers (10,000 records)
def generate_customers():
    start_date = datetime(2023, 1, 1)
    countries = ['US', 'UK', 'CA', 'AU']
    segments = ['New', 'Regular', 'Premium']
    
    customers = {
        'customer_id': range(1, 10001),
        'signup_date': [start_date + timedelta(days=random.randint(0, 365)) for _ in range(10000)],
        'country': [random.choice(countries) for _ in range(10000)],
        'segment': [random.choice(segments) for _ in range(10000)]
    }
    return pd.DataFrame(customers)

# Generate products (1,000 records)
def generate_products():
    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
    products = {
        'product_id': range(1, 1001),
        'category': [random.choice(categories) for _ in range(1000)],
        'price': [round(random.uniform(10, 1000), 2) for _ in range(1000)],
        'cost': [round(random.uniform(5, 800), 2) for _ in range(1000)]
    }
    return pd.DataFrame(products)

# Generate orders and order_items (100,000 records)
def generate_orders_and_items(customers_df, products_df):
    start_date = datetime(2023, 1, 1)
    orders = []
    order_items = []
    
    for order_id in range(1, 100001):
        customer_id = random.choice(customers_df['customer_id'])
        order_date = start_date + timedelta(days=random.randint(0, 365))
        status = random.choice(['Completed', 'Shipped', 'Pending'])
        
        orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date,
            'status': status
        })
        
        # Generate 1-5 items per order
        for _ in range(random.randint(1, 5)):
            product = products_df.sample(1).iloc[0]
            order_items.append({
                'order_id': order_id,
                'product_id': product['product_id'],
                'quantity': random.randint(1, 5),
                'unit_price': product['price']
            })
    
    return pd.DataFrame(orders), pd.DataFrame(order_items)

# Generate and save data
customers_df = generate_customers()
products_df = generate_products()
orders_df, order_items_df = generate_orders_and_items(customers_df, products_df)

# Save to CSV
customers_df.to_csv('customers.csv', index=False)
products_df.to_csv('products.csv', index=False)
orders_df.to_csv('orders.csv', index=False)
order_items_df.to_csv('order_items.csv', index=False)