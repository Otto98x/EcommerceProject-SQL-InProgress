-- Drop tables if they exist (be careful with this in production!)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

-- Create customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    signup_date DATE NOT NULL,
    country VARCHAR(2) NOT NULL,
    segment VARCHAR(10) NOT NULL
);

-- Create products table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL
);

-- Create orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create order_items table
CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_customers_country ON customers(country);
CREATE INDEX idx_customers_segment ON customers(segment);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);