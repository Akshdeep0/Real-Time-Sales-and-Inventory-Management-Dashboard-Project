import pandas as pd
from sqlalchemy import create_engine

# Load the CSV file
csv_file = '/Users/akshdeep/Documents/Project/supermarket_sales.csv'
sales_df = pd.read_csv(csv_file)

# Step 1: Check for missing or null values in 'Invoice ID'
missing_invoice_ids = sales_df[sales_df['Invoice ID'].isnull()]
if not missing_invoice_ids.empty:
    print("Rows with missing 'Invoice ID':")
    print(missing_invoice_ids)
    
    # Option 1: Fill missing 'Invoice ID' with 'Unknown'
    sales_df['Invoice ID'].fillna('Unknown', inplace=True)

    # Option 2: Alternatively, you can drop rows with missing 'Invoice ID' values
    # sales_df.dropna(subset=['Invoice ID'], inplace=True)
else:
    print("No missing 'Invoice ID' found.")

# Step 2: Rename the CSV columns to match the PostgreSQL table columns
sales_df.rename(columns={
    'Invoice ID': 'invoice_id',
    'Branch': 'branch',
    'City': 'city',
    'Customer type': 'customer_type',
    'Gender': 'gender',
    'Product line': 'product_line',
    'Unit price': 'unit_price',
    'Quantity': 'quantity',
    'Tax 5%': 'tax',  # Rename 'Tax 5%' to 'tax'
    'Total': 'total',
    'Date': 'date',
    'Time': 'time',
    'Payment': 'payment',
    'cogs': 'cogs',
    'gross margin percentage': 'gross_margin_percentage',
    'gross income': 'gross_income',
    'Rating': 'rating'
}, inplace=True)

# Step 3: Create PostgreSQL engine
engine = create_engine('postgresql://postgres:postgresp@localhost:5432/sales_inventory_db')

# Step 4: Ingest the CSV into the PostgreSQL table
try:
    sales_df.to_sql('products', engine, if_exists='append', index=False)
    print("Data ingested successfully!")
except Exception as e:
    print(f"An error occurred during data ingestion: {e}")
