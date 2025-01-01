# Data Dictionary

## Raw Data Tables

### customers
- customer_id (PK): Unique identifier
- signup_date: Customer registration date
- country: Customer location
- segment: Customer segment (New/Regular/Premium)

### orders
- order_id (PK): Unique order identifier
- customer_id (FK): Reference to customers
- order_date: Transaction timestamp
- status: Order status

### products
- product_id (PK): Unique product identifier
- category: Product category
- price: Selling price
- cost: Product cost

### order_items
- order_id (FK): Reference to orders
- product_id (FK): Reference to products
- quantity: Items purchased
- unit_price: Price at purchase time
