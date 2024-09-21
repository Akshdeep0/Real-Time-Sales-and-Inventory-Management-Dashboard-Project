import pandas as pd
from sqlalchemy import create_engine, text
from data_cleaning import clean_and_validate_data

# Specify the CSV file path
csv_file = '/Users/akshdeep/Documents/Project/supermarket_sales.csv'

# Step 1: Clean and validate data
sales_df = clean_and_validate_data(csv_file)

# Step 2: Create PostgreSQL engine
engine = create_engine('postgresql://postgres:postgresp@localhost:5432/sales_inventory_db')

# Step 3: Check for existing invoice IDs in the database to avoid duplicates
existing_invoices = pd.read_sql_query("SELECT invoice_id FROM products", engine)
existing_invoice_ids = existing_invoices['invoice_id'].tolist()

# Filter out rows with duplicate invoice_ids that already exist in the database
sales_df = sales_df[~sales_df['invoice_id'].isin(existing_invoice_ids)]
# Function to insert data into sales
def insert_sales():
    with engine.connect() as connection:
        query = text("""
        INSERT INTO sales (invoice_id, sale_date, quantity_sold, total_sale, branch, payment_method, city, customer_type)
        SELECT p.invoice_id, CURRENT_DATE, p.quantity, p.total, p.branch, p.payment, p.city, p.customer_type
        FROM products p
        WHERE NOT EXISTS (SELECT 1 FROM sales s WHERE s.invoice_id = p.invoice_id);
        """)
        connection.execute(query)
        print("Sales data inserted successfully.")

# Function to insert data into inventory
def insert_inventory():
    with engine.connect() as connection:
        query = text("""
        INSERT INTO inventory (invoice_id, stock_quantity, restock_date, product_name, quantity)
        SELECT p.invoice_id, p.quantity, CURRENT_DATE, p.product_line, p.quantity
        FROM products p
        WHERE NOT EXISTS (SELECT 1 FROM inventory i WHERE i.invoice_id = p.invoice_id);
        """)
        connection.execute(query)
        print("Inventory data inserted successfully.")

# Ingest data into the sales and inventory tables
insert_sales()
insert_inventory()
if not sales_df.empty:
    # Step 4: Ingest the cleaned data into the PostgreSQL table
    try:
        sales_df.to_sql('products', engine, if_exists='append', index=False)
        print("Data ingested successfully!")
    except Exception as e:
        print(f"An error occurred during data ingestion: {e}")
else:
    print("No new data to ingest. All records already exist in the database.")
