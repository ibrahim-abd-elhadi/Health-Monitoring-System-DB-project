import mysql.connector
import time
import random
from datetime import datetime

# Function to insert data into the Health_Metrics table
def insert_health_metrics(patient_id, connection):
    cursor = connection.cursor()
    
    # Generate random values for health metrics (replace with real sensor data if available)
    heart_rate = random.randint(60, 100)  # Random heart rate between 60 and 100
    blood_pressure = f"{random.randint(110, 130)}/{random.randint(70, 90)}"  # Random blood pressure
    activity_level = random.choice(['Low', 'Medium', 'High'])  # Random activity level
    sleep_quality = random.choice(['Good', 'Average', 'Poor'])  # Random sleep quality
    wellness = random.choice(['Excellent', 'Good', 'Fair', 'Poor'])  # Random wellness status
    
    # Prepare the SQL query
    query = """
        INSERT INTO Health_Metrics (patient_id, heart_rate, blood_pressure, activity_level, sleep_quality, wellness, date_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Data to insert
    data = (patient_id, heart_rate, blood_pressure, activity_level, sleep_quality, wellness, current_time)
    
    try:
        # Execute the query
        cursor.execute(query, data)
        connection.commit()
        print(f"Inserted data for patient {patient_id} at {current_time}")
    except mysql.connector.Error as err:
        print(f"Error inserting data for patient {patient_id}: {err}")
    finally:
        cursor.close()

# Connect to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='AQI',  # Hostname or IP address of your MySQL server
            port=3306,  # MySQL default port
            user='root',  # Your MySQL username
            password='AQI.ib1235879',  # Replace with your MySQL password
            database='healthcaresystem'  # Replace with your database name
        )
        print("Database connection established.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        exit(1)

# Function to fetch all patient IDs
def get_all_patients(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT patient_id FROM Patients")  # Query to fetch all patient IDs
        patients = cursor.fetchall()
        return [patient['patient_id'] for patient in patients]  # Return list of patient IDs
    except mysql.connector.Error as err:
        print(f"Error fetching patient IDs: {err}")
        return []
    finally:
        cursor.close()

# Main function to repeatedly insert health data for all patients
def main():
    connection = create_connection()
    
    try:
        patients = get_all_patients(connection)  # Get all patient IDs from the database
        if not patients:
            print("No patients found in the database. Exiting.")
            return
        
        while True:
            # Loop through all patients and insert data for each
            for patient_id in patients:
                insert_health_metrics(patient_id, connection)
            
            # Wait for 1 second before inserting again for the next set of patients
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Data insertion stopped.")
    
    finally:
        # Close the connection when done
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
