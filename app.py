from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from datetime import date, time, datetime

app = Flask(__name__)

# Create a connection to the PostgreSQL database
engine = create_engine('postgresql://postgres:password@localhost:5432/sales_inventory_db')

# Helper function to convert row to a dictionary and handle non-serializable objects
def row_to_dict(row):
    row_dict = dict(row._mapping)
    # Convert any non-serializable objects to strings (e.g., date, time, datetime)
    for key, value in row_dict.items():
        if isinstance(value, (date, time, datetime)):
            row_dict[key] = value.isoformat()  # Convert to ISO format string
    return row_dict

# Route to fetch products from the 'products' table
@app.route('/products', methods=['GET'])
def get_products():
    with engine.connect() as connection:
        query = text("SELECT * FROM products")
        rows = connection.execute(query)
        data = [row_to_dict(row) for row in rows]
    return jsonify(data)

# Route to fetch sales from the 'sales' table
@app.route('/sales', methods=['GET'])
def get_sales():
    with engine.connect() as connection:
        query = text("SELECT * FROM sales")
        rows = connection.execute(query)
        data = [row_to_dict(row) for row in rows]
    return jsonify(data)

# Route to fetch inventory from the 'inventory' table
@app.route('/inventory', methods=['GET'])
def get_inventory():
    with engine.connect() as connection:
        query = text("SELECT * FROM inventory")
        rows = connection.execute(query)
        data = [row_to_dict(row) for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
