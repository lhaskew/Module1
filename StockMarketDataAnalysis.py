import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Importing the dataset.
file = 'MSHistoricalData.csv'

# Check if the CSV file exists and load it.
if not os.path.exists(file):
    raise FileNotFoundError(f"{file} not found.")

df = pd.read_csv(file)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Current date range selected from the Microsoft Stock Market data.
min_date = datetime(2023, 10, 5)
max_date = datetime(2024, 10, 4)

# This section goes over the user input classifications.
def user_selection():
    while True:
        choice = input("MS Last Year Stock Market Data\nWould you like to see the entire dataset or a specific date range? ('entire'/'range'): ").strip().lower()
        
        if choice == 'entire':
            return None, None, 1
        
        elif choice == 'range':
            start_date = input("Enter start date (MM/DD/YYYY): ")
            end_date = input("Enter end date (MM/DD/YYYY): ")
            
            try:
                start = datetime.strptime(start_date, '%m/%d/%Y')
                end = datetime.strptime(end_date, '%m/%d/%Y')
            except ValueError:
                print("Invalid date format. Use MM/DD/YYYY.")
                continue
            
            if not (min_date <= start <= max_date):
                print(f"Start date must be between {min_date.strftime('%m/%d/%Y')} and {max_date.strftime('%m/%d/%Y')}.")
                continue
            if not (min_date <= end <= max_date):
                print(f"End date must be between {min_date.strftime('%m/%d/%Y')} and {max_date.strftime('%m/%d/%Y')}.")
                continue
            if start > end:
                print("The start date cannot be after the end date.")
                continue
            
            option = input("Choose an option: \n1. Show all data in selected date range \n2. Start to end date market difference \n3. Average start to end date market\n")
            if option not in ['1', '2', '3']:
                print("Invalid option. Please select 1, 2, or 3.")
                continue
            
            return start_date, end_date, int(option)
        
        else:
            print("Invalid choice. Please enter 'entire' or 'range'.")

# Date/Time rules.
def filter_data(start_date, end_date):
    start = datetime.strptime(start_date, '%m/%d/%Y')
    end = datetime.strptime(end_date, '%m/%d/%Y')
    filtered_df = df[(df['Date'] >= start) & (df['Date'] <= end)]
    if filtered_df.empty:
        raise ValueError("No data found in the specified date range.")
    return filtered_df

# Saves the CSV files with separate names per option.
def save_to_csv(data, filename):
    try:
        data.to_csv(filename, index=False)
        print(f"Data has been saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")

def AllData(data):
    save_to_csv(data, 'all_data.csv')

def ShowRangeData(data):
    save_to_csv(data, 'range_data.csv')

# Gives the difference in data from start to end for selected range.
def StartEndRange(data):
    start_data = data.iloc[0]
    end_data = data.iloc[-1]

    start_data_numeric = start_data[1:].apply(pd.to_numeric, errors='coerce')
    end_data_numeric = end_data[1:].apply(pd.to_numeric, errors='coerce')

    diff = end_data_numeric - start_data_numeric
    diff_df = pd.DataFrame(diff).transpose()
    diff_df['Date'] = "Difference"
    print(diff_df)

# Gives the data average for selected range.
def StartEndAverage(data):
    avg_data = data.mean(numeric_only=True)
    avg_df = pd.DataFrame(avg_data).transpose()
    avg_df['Date'] = "Average"
    print(avg_df)
    return avg_df

# Creates the graph based on the user selection.
def graph_data(data):
    plt.figure(figsize=(10, 6))
    for column in ['Close/Last', 'Volume', 'Open', 'High', 'Low']:
        if column in data.columns:
            plt.plot(data['Date'], data[column], label=column)
    plt.title('Microsoft Previous Year Stock Market Data')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.show()

# Main function allowing user input.
def main():
    while True:
        try:
            start_date, end_date, option = user_selection()
            
            if option == 1:
                if start_date is None and end_date is None:
                    AllData(df)
                    user_input_visual = input("Would you like to create a visual of the entire dataset? (y/n): ").strip().lower()
                    if user_input_visual == 'y':
                        graph_data(df)
                else:
                    filtered_data = filter_data(start_date, end_date)
                    ShowRangeData(filtered_data)
                    user_input_visual = input("Would you like to create a visual of the selected data range? (y/n): ").strip().lower()
                    if user_input_visual == 'y':
                        graph_data(filtered_data)
            else:
                filtered_data = filter_data(start_date, end_date)

                if option == 2:
                    StartEndRange(filtered_data)
                elif option == 3:
                    avg_df = StartEndAverage(filtered_data)
                    user_input_visual = input("Would you like to create a visual of the average data? (y/n): ").strip().lower()
                    if user_input_visual == 'y':
                        graph_data(avg_df)

                user_input_visual = input("Would you like to create a visual of the filtered data? (y/n): ").strip().lower()
                if user_input_visual == 'y':
                    graph_data(filtered_data)

            continue_input = input("Would you like to perform another operation? (y/n): ").strip().lower()
            if continue_input != 'y':
                print("Exiting the program.")
                break

        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

