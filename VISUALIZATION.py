import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def demand_visualization():
    csv_file_path = r'C:\Users\achyu\Downloads\ANDHRA PRADESH DATA.csv'
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()
    date_column_name = 'DATE'
    demand_column_name = 'ENERGY DEMAND'
    df[date_column_name] = pd.to_datetime(df[date_column_name], format="%d-%m-%Y")
    df.set_index(date_column_name, inplace=True)
# plotting
    plt.figure(figsize=(16,8 ))
    plt.plot(df.index, df[demand_column_name], label='Electrical Demand',color = 'black')
    plt.title('State Electrical Demand Over 5 Years')
    plt.xlabel('Date')
    plt.ylabel('Electrical Demand (MW)')
    plt.style.use('fivethirtyeight')
    plt.grid(True)
    plt.xticks(rotation=360)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    demand_visualization()