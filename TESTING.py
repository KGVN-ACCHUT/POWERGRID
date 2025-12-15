import pandas as pd
import numpy as np

UNIT_DEMAND_MW = 170
FILE_NAME = r'C:\Users\achyu\Downloads\ANDHRA PRADESH DATA.csv'

def testing():
    df = pd.read_csv(FILE_NAME)
    df.columns = df.columns.str.strip()
    demand_col = 'ENERGY DEMAND'
    df.rename(columns={demand_col: 'Demand_MW'}, inplace=True)
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d-%m-%Y')
    df['Date'] = df['DATE'].dt.date
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    min_date_str = min_date.strftime('%d-%m-%Y')
    max_date_str = max_date.strftime('%d-%m-%Y')
    print("=" * 60)
    print(f"Data Date Range: {min_date_str} to {max_date_str}")
    print("=" * 60)
    date_input_str = input(f"\nEnter the date you want to analyze (Format: DD-MM-YYYY): ")
    try:
        selected_date = pd.to_datetime(date_input_str, format='%d-%m-%Y').date()
    except Exception:
        raise ValueError("Invalid date format entered. Please use DD-MM-YYYY.")
    if selected_date < min_date or selected_date > max_date:
        print("\nERROR: The given date is outside the data range.")
        print(f"Please enter a date between {min_date_str} and {max_date_str}.")
        exit()
    selected_date_str = selected_date.strftime('%d-%m-%Y')
    daily_data = df[df['Date'] == selected_date].copy()
    avg_daily_demand_mw = daily_data['Demand_MW'].mean()
    percentage_of_total_demand = (UNIT_DEMAND_MW / avg_daily_demand_mw) * 100
    daily_data['Simulated_Demand_MW'] = daily_data['Demand_MW'] - UNIT_DEMAND_MW
    simulated_avg_daily_demand_mw = daily_data['Simulated_Demand_MW'].mean()
    demand_percentage_drop = ((avg_daily_demand_mw - simulated_avg_daily_demand_mw) / avg_daily_demand_mw) * 100
    print("=" * 60)
    print("\n==== Analysis for Selected Day:", selected_date_str, "====")
    print("\tOriginal Average Daily Demand:", f"{avg_daily_demand_mw:.2f}", "MW")
    print("\tOffline Industrial Unit Demand:", UNIT_DEMAND_MW, "MW")
    print("\tRemaining Net Demand:", f"{simulated_avg_daily_demand_mw:.2f}", "MW")
    print("=" * 60)
    print("====Demand Percentage Drop====")
    print(f"\n1. The {UNIT_DEMAND_MW} MW unit represents:")
    print(f"\t{percentage_of_total_demand:.2f}%% of the Average Daily Demand.")
    print("\n2. The demand percentage drop would be:")
    print(f"\t{demand_percentage_drop:.2f}%%")
    print("=" * 60)

if __name__ == "__main__":
    testing()
