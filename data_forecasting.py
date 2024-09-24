import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_sales(file_path, forecast_steps=10):
    """
    Forecast sales using Exponential Smoothing.

    Parameters:
    - file_path: Path to the sales data CSV file.
    - forecast_steps: Number of periods to forecast.

    Returns:
    - forecast: The forecasted values as a Pandas Series.
    """

    # Load the sales data from the CSV file
    df = pd.read_csv(file_path)

    # Example: Using the 'Total' column for forecasting
    data = df['Total']

    # Train the Exponential Smoothing model
    model = ExponentialSmoothing(data, trend='add', seasonal='add', seasonal_periods=12)
    model_fit = model.fit()

    # Forecast future sales
    forecast = model_fit.forecast(steps=forecast_steps)

    # Print the forecasted values
    print(f"Forecast for next {forecast_steps} periods:")
    print(forecast)

    return forecast

# Example of forecasting inventory using a simple mean calculation
def forecast_inventory(csv_file):
    # Load the data
    df = pd.read_csv(csv_file)

    # Apply your logic for forecasting inventory
    # This is a placeholder example of calculating the average quantity
    avg_inventory = df['Quantity'].mean()

    # Forecast for the next 10 periods as an example
    forecast = pd.Series(np.random.normal(avg_inventory, 5, 10))
    print("Inventory forecast for next 10 periods:")
    print(forecast)
    
    return forecast

# Example of forecasting demand based on a simple rolling average
def forecast_demand(csv_file):
    # Load the data
    df = pd.read_csv(csv_file)
    
    # Apply your logic for forecasting demand
    # This is a placeholder example using the quantity column
    avg_demand = df['Quantity'].rolling(window=3).mean().iloc[-1]  # Calculate a rolling average
    
    # Forecast for the next 10 periods as an example
    forecast = pd.Series(np.random.normal(avg_demand, 5, 10))
    
    print("Demand forecast for next 10 periods:")
    print(forecast)
    
    return forecast