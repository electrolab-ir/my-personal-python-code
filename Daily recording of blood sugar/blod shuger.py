import sqlite3
import pandas as pd
from datetime import datetime

# Database setup
conn = sqlite3.connect('blood_sugar.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS blood_sugar (
    id INTEGER PRIMARY KEY,
    measurement REAL,
    timestamp TEXT,
    context TEXT
)
''')
conn.commit()

def add_measurement(measurement, context):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO blood_sugar (measurement, timestamp, context) VALUES (?, ?, ?)', (measurement, timestamp, context))
    conn.commit()
    print(f'Measurement {measurement} added at {timestamp} with context {context}.')

def export_to_csv():
    df = pd.read_sql_query('SELECT * FROM blood_sugar', conn)
    df.to_csv('blood_sugar_measurements.csv', index=False)
    print('Data exported to blood_sugar_measurements.csv')

def main():
    while True:
        print("\n1. Add blood sugar measurement")
        print("2. Export data to CSV")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            try:
                measurement = float(input("Enter blood sugar measurement: "))
                print("\nSelect the context of the blood sugar measurement:")
                print("1. Fasting")
                print("2. Before Breakfast")
                print("3. After Breakfast")
                print("4. Before Lunch")
                print("5. After Lunch")
                print("6. Before Dinner")
                print("7. After Dinner")
                
                context_choice = input("Enter your choice: ")
                context_dict = {
                    '1': 'Fasting',
                    '2': 'Before Breakfast',
                    '3': 'After Breakfast',
                    '4': 'Before Lunch',
                    '5': 'After Lunch',
                    '6': 'Before Dinner',
                    '7': 'After Dinner'
                }
                
                context = context_dict.get(context_choice, 'Unknown')
                add_measurement(measurement, context)
            except ValueError:
                print("Invalid measurement. Please enter a number.")
        elif choice == '2':
            export_to_csv()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()