# Took the data of 5 years electtical demand. Used four years for the taining period and used last one year for the testing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_PATH = r'C:\Users\achyu\Downloads\ANDHRA PRADESH DATA.csv'
DATE_COLUMN = 'DATE'
DEMAND_COLUMN = 'ENERGY DEMAND'
WINDOW_SIZE = 30
# MAPE claculation
def calculate_mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero_mask = y_true != 0
    percentage_error = np.abs((y_true[non_zero_mask] - y_pred[non_zero_mask]) / y_true[non_zero_mask]) * 100
    return percentage_error.mean()
print("--- Starting Electricity Demand Forecast with 4-Year Split ---")
# Load data
def moving_average():
    data = pd.read_csv(
        FILE_PATH,
        parse_dates=[DATE_COLUMN],
        index_col=DATE_COLUMN
    )
    data.columns = data.columns.str.strip()
    data = data[[DEMAND_COLUMN]].dropna()
    total_records = len(data)
    data.index = pd.to_datetime(data.index, dayfirst=True)
#split
    date_diff = data.index.max() - data.index.min()
    total_days = date_diff.days
    total_years = total_days / 365.25
    train_size = int(total_records * 0.8)
    split_date = data.index[train_size]
    print(f"\nTotal Data Span: {total_years:.2f} years ({total_records} records)")
    print(f"Training Data (4 Years): {train_size} records, up to {split_date}")
    print(f"Testing Data (1 Year): {total_records - train_size} records")
#Moving Average
    data['MA_Forecast'] = data[DEMAND_COLUMN].rolling(window=WINDOW_SIZE).mean().shift(1)
    data_forecasted = data.dropna()
    print(f"Moving Average calculated using a window of {WINDOW_SIZE} periods.")
    train_data = data_forecasted.loc[:split_date]
    test_data = data_forecasted.loc[split_date:]
    actual_values = test_data[DEMAND_COLUMN]
    predicted_values = test_data['MA_Forecast']
    mape_score = calculate_mape(actual_values, predicted_values)
    print("\n--- Forecast Evaluation Results (5th Year) ---")
    print(f"Test Period Length: {len(test_data)} observations")
    print(f"**Mean Absolute Percentage Error (MAPE): {mape_score:.2f}%**")
    print("\nInterpretation: The Moving Average forecast's average error in the final year is {:.2f}%.".format(mape_score))
# plotting
    plt.figure(figsize=(14, 7))
    plt.plot(train_data[DEMAND_COLUMN], label='Training Actual Demand (4 Years)', color='yellow')
    plt.plot(train_data['MA_Forecast'], label=f'MA Forecast (Training)', color='green' )
    plt.plot(test_data[DEMAND_COLUMN], label='Testing Actual Demand (5th Year)', color='blue')
    plt.plot(predicted_values, label=f'MA Forecast (Testing)', color='black')
    plt.axvspan(test_data.index[0], test_data.index[-1], color='black', alpha=0.1, label='1-Year Test Period')
    plt.title(f'Demand Forecast: {WINDOW_SIZE}-Period MA (4 Years Train / 1 Year Test)')
    plt.xlabel(DATE_COLUMN)
    plt.ylabel(DEMAND_COLUMN)
    plt.legend()
    plt.grid(True,)
    plt.tight_layout()
    plt.show()
if __name__ == '__main__':
    moving_average()
