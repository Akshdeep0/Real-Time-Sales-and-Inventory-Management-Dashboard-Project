import pandas as pd

def clean_and_validate_data(csv_file):
    # Load the CSV file
    sales_df = pd.read_csv(csv_file)
    
    # Step 1: Check for missing or null values in 'Invoice ID'
    missing_invoice_ids = sales_df[sales_df['Invoice ID'].isnull()]
    if not missing_invoice_ids.empty:
        print("Rows with missing 'Invoice ID':")
        print(missing_invoice_ids)
        
        # Option 1: Fill missing 'Invoice ID' with 'Unknown'
        sales_df['Invoice ID'].fillna('Unknown', inplace=True)
        
        # Option 2: Alternatively, drop rows with missing 'Invoice ID'
        # sales_df.dropna(subset=['Invoice ID'], inplace=True)
    else:
        print("No missing 'Invoice ID' found.")
    
    # Step 2: Remove duplicate 'Invoice ID' entries
    sales_df.drop_duplicates(subset=['Invoice ID'], inplace=True)
    
    # Step 3: Rename the CSV columns to match the PostgreSQL table columns
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
    
    # Step 4: Perform additional data validation (e.g., check for negative values)
    if (sales_df['unit_price'] < 0).any():
        print("Warning: Some unit prices are negative.")
    
    if (sales_df['quantity'] < 0).any():
        print("Warning: Some quantities are negative.")
    
    return sales_df
