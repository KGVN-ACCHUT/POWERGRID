import pandas as pd
import numpy as np


def detect_and_research_anomalies():
    num_anomalies = 10 # number of anamolies 
    csv_file_path = r'C:\Users\achyu\Downloads\ANDHRA PRADESH DATA.csv'
    df = pd.read_csv(csv_file_path) # command to read the file
    df.columns = df.columns.str.strip() # command to clear the empty spaces in the file
    date_column_name = 'DATE'
    demand_column_name = 'ENERGY DEMAND'
    df[date_column_name] = pd.to_datetime(df[date_column_name], format="%d-%m-%Y")
    df.set_index(date_column_name, inplace=True)
    window_size = 30
#Z-Score-calculation (core logic)
    df['Rolling_Mean'] = df[demand_column_name].rolling(window=window_size, center=True).mean() # defining the logic for rolling mean
    df['Rolling_Std'] = df[demand_column_name].rolling(window=window_size, center=True).std() # defing the logic for rolling standard
    df['Z_Score'] = (df[demand_column_name] - df['Rolling_Mean']) / df['Rolling_Std'] # definf the z_score
    df['Abs_Z_Score'] = df['Z_Score'].abs() # defing the logic for absolute z_score
    top_anomalies = df.nlargest(num_anomalies, 'Abs_Z_Score') # defining the logic for top_anamolies
    print(f"\n Top {num_anomalies} Electrical Demand Anomaly Dates ---")
#output
    anomaly_list = []
    for date, row in top_anomalies.iterrows():
        anomaly_type = "Spike (High Demand)" if row['Z_Score'] > 0 else "Drop (Low Demand)"
        anomaly_list.append({
            "Date": date.strftime('%Y-%m-%d'),
            "Demand (MW)": f"{row[demand_column_name]:.2f}",
            "Z-Score": f"{row['Z_Score']:.2f}",
            "Anomaly Type": anomaly_type
        })
    results_df = pd.DataFrame(anomaly_list)
    print(results_df.to_markdown(index=False))

if  __name__ == "__main__":
    detect_and_research_anomalies()
