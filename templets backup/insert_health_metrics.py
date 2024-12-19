import mysql.connector
import time
import random
from datetime import datetime

def insert_health_metrics(patient_id, connection):
    cursor = connection.cursor()

    # Generate random values for health metrics
    heart_rate = random.randint(60, 150)  # Random heart rate
    blood_pressure = f"{random.randint(110, 130)}/{random.randint(70, 90)}"  # Random blood pressure
    blood_sugar = round(random.uniform(70, 500), 2)  # Random blood sugar (mg/dL)
    activity_level = random.choice(['Low', 'Medium', 'High'])
    sleep_quality = random.choice(['Good', 'Average', 'Poor'])
    

    # Prepare the SQL query
    query = """
        INSERT INTO Health_Metrics 
        (patient_id, heart_rate, blood_pressure, blood_sugar, activity_level, sleep_quality,  date_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Data to insert
    data = (patient_id, heart_rate, blood_pressure, blood_sugar, activity_level, sleep_quality, current_time)

    try:
        
        cursor.execute(query, data)
        connection.commit()
        print(f"Inserted data for patient {patient_id} at {current_time}")
    except mysql.connector.Error as err:
        print(f"Error inserting data for patient {patient_id}: {err}")
    finally:
        cursor.close()


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='AQI',  
            port=3306,  
            user='root',  
            password='password',  
            database='healthcaresystem'  
        )
        print("Database connection established.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        exit(1)


def get_all_patients(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT patient_id FROM Patients")  
        patients = cursor.fetchall()
        return [patient['patient_id'] for patient in patients]  
    except mysql.connector.Error as err:
        print(f"Error fetching patient IDs: {err}")
        return []
    finally:
        cursor.close()


def main():
    connection = create_connection()
    
    try:
        patients = get_all_patients(connection)  
        if not patients:
            print("No patients found in the database. Exiting.")
            return
        
        while True:
            
            for patient_id in patients:
                insert_health_metrics(patient_id, connection)
            
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Data insertion stopped.")
    
    finally:
        
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
