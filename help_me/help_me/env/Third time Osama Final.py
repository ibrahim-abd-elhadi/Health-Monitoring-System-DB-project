from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector
from collections import deque

# Database Connection Function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='admin',  # Update your MySQL password here
            database='healthcaresystem'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        exit(1)

# Initialize Flask Application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for flash messages and session management

# Routes

## Login Page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = create_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user is None:
            flash('Email or password is incorrect', 'error')
            return render_template('login.html')
        elif user[5].lower() == 'patient':
            flash('Login successful!', 'success')
            session['user_id'] = user[0]  # Assuming `user[0]` is `user_id`
            return redirect(url_for('patientpagedashboard'))     #333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
        elif user[5].lower() == 'doctor':
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid user role.', 'error')

    return render_template('login.html', error=error)

## Account Type Selection
@app.route('/which', methods=['GET', 'POST'])
def which():
    if request.method == 'POST':
        account_type = request.form['account_type']
        if account_type == 'doctor':
            return redirect(url_for('doctor_profile_signup'))
        elif account_type == 'patient':
            return redirect(url_for('patient_profile_signup'))
    return render_template('Account_Type.html')

## Doctor Profile Signup
@app.route('/doctor_profile_signup', methods=['GET', 'POST'])
def doctor_profile_signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone = request.form.get('phone', '')
        gender = request.form.get('gender')
        age = request.form.get('age', 0)
        role = 'doctor'

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('doctor_profile_signup'))

        connection = create_connection()
        cursor = connection.cursor()
        query_check_email = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already exists! Please log in.', 'danger')
            return redirect(url_for('login'))

        query = """
            INSERT INTO users (name, email, password, phone, role, gender, age)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_name, email, password, phone, role, gender, age))

        connection.commit()
        cursor.close()
        connection.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))                 #3333333333333333333333333333333333333333333

    return render_template('doctor_profile_signup.html')


#------------------------------------------------------------------------------------------------------------------------------
## Patient Profile Signup
@app.route('/patient_profile_signup', methods=['GET', 'POST'])
def patient_profile_signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone = request.form.get('phone', '')
        gender = request.form.get('gender')
        age = request.form.get('age', 0)
        role = 'patient'

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('patient_profile_signup'))

        connection = create_connection()
        cursor = connection.cursor()
        query_check_email = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already exists! Please log in.', 'danger')
            return redirect(url_for('login'))

        query = """
            INSERT INTO users (name, email, password, phone, role, gender, age)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """


        cursor.execute(query, (user_name, email, password, phone, role, gender, age))

        user_id = cursor.lastrowid
        session['user_id'] = user_id  # Save user ID in session

        connection.commit()
        cursor.close()
        connection.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('patient_details'))

    return render_template('patient_profile_signup.html')

## Patient Details
@app.route('/patient_details', methods=['GET', 'POST'])
def patient_details():
    user_id = session.get('user_id', None)

    if user_id is None:
        flash('User is not logged in!', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        health_history = request.form.get('health-history', '')
        emergency_contacts = request.form.getlist('emergency-contact')
        emergency_contacts_str = ','.join(emergency_contacts)

        connection = create_connection()
        cursor = connection.cursor()
        #query = """
        #    INSERT INTO patients (patient_id, height, weight, blood_type, chronic_conditions, emergency_contact)
        #    VALUES (%s, %s, %s, 'NULL' , %s, %s)
        #"""




        # الخطوة 1: الحصول على آخر user_id من جدول users
        query_last_user_id = "SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1"

        try:
        #    تنفيذ الاستعلام للحصول على آخر user_id
            cursor.execute(query_last_user_id)
            last_user_id = cursor.fetchone()

            if last_user_id:
                user_id = last_user_id[0]  # استخراج آخر user_id

                # الخطوة 2: إدخال user_id في جدول patients
                query_insert_patient = """
                    INSERT INTO patients (patient_id, height, weight, blood_type, chronic_conditions, emergency_contact) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                # استبدل القيم المناسبة هنا
                patient_data = (user_id, height, weight, '+a', 'None', emergency_contacts_str)

                cursor.execute(query_insert_patient, patient_data)
                connection.commit()  # حفظ التغييرات في قاعدة البيانات
                flash("New patient added successfully.")
            else:
                flash("No users found in the database.")
        except Exception as e:
            flash(f"An error occurred: {e}")


#        query = """UPDATE patients SET height = %s, weight = %s, health_history = %s, emergency_contact = %s WHERE patient_id = 4 """

#        cursor.execute(query, (user_id, height, weight, health_history, emergency_contacts_str))

        connection.commit()
        cursor.close()
        connection.close()

        flash('Patient details saved successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('patient_details.html', user_id=user_id)



#--------------------------------------------------------------------------------------------------------------------#
## Home Page

health_trend_queue = deque([70, 72, 74, 76, 78, 80, 82], maxlen=7)
@app.route('/index')
def index():
    # Sample data from database
    #activity = 70  # Example value
    # sleep = 25     # Example value
    # wellness = 30  # Example value
    #health_trend = [70, 72, 74, 76, 78, 80, 82]  # Example trend data

    # Pass data to the HTML
    #return render_template('index.html', activity=activity, sleep=sleep, wellness=wellness, health_trend=health_trend)
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Query the total number of rows for activity levels
        cursor.execute("SELECT COUNT(*) FROM health_metrics WHERE activity_level IN ('High', 'Medium', 'Low')")
        total_activity_rows = cursor.fetchone()[0]

        # Query to count occurrences of each activity level
        query_activity = """
            SELECT 
                activity_level, 
                COUNT(*) AS count 
            FROM 
                health_metrics 
            WHERE 
                activity_level IN ('High', 'Medium', 'Low')
            GROUP BY 
                activity_level;
        """
        cursor.execute(query_activity)
        results_activity = cursor.fetchall()

        # Parse activity results
        counts_activity = {row[0]: row[1] for row in results_activity}
        counts_activity.setdefault('High', 0)
        counts_activity.setdefault('Medium', 0)
        counts_activity.setdefault('Low', 0)

        # Calculate activity average
        avg_high = counts_activity['High']*2 / total_activity_rows if total_activity_rows > 0 else 0
        avg_medium = counts_activity['Medium']*1.2 / total_activity_rows if total_activity_rows > 0 else 0
        avg_low = counts_activity['Low']*0.9 / total_activity_rows if total_activity_rows > 0 else 0
        activity = (avg_high + avg_medium + avg_low) / 3

        # Query the total number of rows for sleep quality
        cursor.execute("SELECT COUNT(*) FROM health_metrics WHERE sleep_quality IN ('Good', 'Average', 'Poor')")
        total_sleep_rows = cursor.fetchone()[0]

        # Query for sleep quality
        query_sleep = """
            SELECT 
                sleep_quality, 
                COUNT(*) AS count 
            FROM 
                health_metrics 
            WHERE 
                sleep_quality IN ('Good', 'Average', 'Poor')
            GROUP BY 
                sleep_quality;
        """
        cursor.execute(query_sleep)
        results_sleep = cursor.fetchall()

        # Parse sleep results
        counts_sleep = {row[0]: row[1] for row in results_sleep}
        counts_sleep.setdefault('Good', 0)
        counts_sleep.setdefault('Average', 0)
        counts_sleep.setdefault('Poor', 0)

        # Calculate sleep average
        avg_good = counts_sleep['Good']*2 / total_sleep_rows if total_sleep_rows > 0 else 0
        avg_average = counts_sleep['Average']*1.2 / total_sleep_rows if total_sleep_rows > 0 else 0
        avg_poor = counts_sleep['Poor']*0.9 / total_sleep_rows if total_sleep_rows > 0 else 0
        sleep = (avg_good + avg_average + avg_poor) / 3

        # Query the total number of rows for wellness
        cursor.execute("SELECT COUNT(*) FROM health_metrics WHERE wellness IN ('Excellent', 'Good', 'Fair', 'Poor')")
        total_wellness_rows = cursor.fetchone()[0]

        # Query for wellness
        query_wellness = """
            SELECT 
                wellness, 
                COUNT(*) AS count 
            FROM 
                health_metrics 
            WHERE 
                wellness IN ('Excellent', 'Good', 'Fair', 'Poor')
            GROUP BY 
                wellness;
        """
        cursor.execute(query_wellness)
        results_wellness = cursor.fetchall()

        # Parse wellness results
        counts_wellness = {row[0]: row[1] for row in results_wellness}
        counts_wellness.setdefault('Excellent', 0)
        counts_wellness.setdefault('Good', 0)
        counts_wellness.setdefault('Fair', 0)
        counts_wellness.setdefault('Poor', 0)

        # Calculate wellness average
        avg_excellent = counts_wellness['Excellent']*2.5 / total_wellness_rows if total_wellness_rows > 0 else 0
        avg_good = counts_wellness['Good']*2 / total_wellness_rows if total_wellness_rows > 0 else 0
        avg_fair = counts_wellness['Fair']*1.2 / total_wellness_rows if total_wellness_rows > 0 else 0
        avg_poor = counts_wellness['Poor']*0.9 / total_wellness_rows if total_wellness_rows > 0 else 0
        wellness = (avg_excellent + avg_good + avg_fair + avg_poor) / 4

        # Calculate health trend as the average of the three averages
        new_health_trend = (activity + sleep + wellness)*100 / 3

        # Update the health trend queue
        health_trend_queue.append(new_health_trend)
        print(health_trend_queue)
        
        #Not WOrking properly For Some reason _+__+_=-=-=-=-=-----------=0=-=90p-0980-0-0-0-0-0-0-0-0-0-0-80-80-80
        
        # # Query 1: Get patient_id with highest health metrics
        # cursor.execute("""
        #     SELECT patient_id 
        #     FROM health_metrics
        #     ORDER BY (heart_rate + blood_Sugar + blood_pressure) DESC 
        #     LIMIT 1;
        # """)
        # highest_patient_id = cursor.fetchone()
        # if highest_patient_id:
        #     cursor.execute("SELECT name FROM users WHERE patient_id = %s", (highest_patient_id[0],))
        #     highest_name = cursor.fetchone()
        #     highest_name = highest_name[0] if highest_name else "Unknown"
        # else:
        #     highest_name = "Unknown"

        # # Query 2: Get patient_id with lowest health metrics
        # cursor.execute("""
        #     SELECT patient_id 
        #     FROM health_metrics
        #     ORDER BY (heart_rate + blood_Sugar + blood_pressure) ASC 
        #     LIMIT 1;
        # """)
        # lowest_patient_id = cursor.fetchone()
        # if lowest_patient_id:
        #     cursor.execute("SELECT name FROM users WHERE patient_id = %s", (lowest_patient_id[0],))
        #     lowest_name = cursor.fetchone()
        #     lowest_name = lowest_name[0] if lowest_name else "Unknown"
        # else:
        #     lowest_name = "Unknown"

        # # Query 3: Get patient_id with moderate health metrics
        # cursor.execute("""
        #     SELECT patient_id 
        #     FROM health_metrics
        #     WHERE heart_rate < 160 
        #     AND blood_Sugar < 200 
        #     AND blood_pressure < 300
        #     LIMIT 1;
        # """)
        # moderate_patient_id = cursor.fetchone()
        # if moderate_patient_id:
        #     cursor.execute("SELECT name FROM users WHERE patient_id = %s", (moderate_patient_id[0],))
        #     moderate_name = cursor.fetchone()
        #     moderate_name = moderate_name[0] if moderate_name else "Unknown"
        # else:
        #     moderate_name = "Unknown"



        #print(highest_name)
        #print(lowest_name)
        #print(moderate_name)







    finally:
        cursor.close()
        connection.close()

    # Pass the averages to the HTML
    return render_template(
        'index.html',
        activity=int(100*activity),
        sleep=int(100*sleep),
        wellness=int(100*wellness),
        health_trend=list(health_trend_queue)  # Pass the queue as a list to the template
        #highest_name=highest_name,
        #lowest_name=lowest_name,
        #moderate_name=moderate_name
    )






#--------------------------------------------------------------------------------------------------------------------#

# Queues for rolling data
blood_sugar_queue = deque([70, 80, 75, 85, 80], maxlen=5)
blood_pressure_queue = deque([70, 80, 75, 85, 80], maxlen=5)
heart_rate_queue = deque([70, 80, 75, 85, 80], maxlen=5)
activity_growth_queue = deque([65, 59, 80, 81, 56, 55, 90, 60, 85, 90, 75, 95], maxlen=12)

@app.route('/patientpagedashboard')
def patientpagedashboard():
# Get user_id from session
    user_id = session.get('user_id', None)
    if not user_id:
        # Redirect to login if user_id is not in session
        return redirect('/login')

    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Query to fetch height and weight for the given patient_id
        cursor.execute("""
            SELECT height, weight 
            FROM patients 
            WHERE patient_id = %s
        """, (user_id,))
        result = cursor.fetchone()

        # Explicitly consume the cursor to avoid issues
        cursor.fetchall()

        if not result:
            # Handle case where no patient is found
            return render_template('error.html', message="Patient not found")

        height, weight = result

        # Calculate BMI
        bmi = weight / ((height / 100) ** 2)  # Convert height to meters
        bmi = f"{bmi:.1f}"  # Format BMI to 1 decimal place

        # Calculate BMI percentage
        ideal_bmi = 22  # Assuming 22 is the ideal BMI
        bmi_percentage = max(0, 100 - abs((float(bmi) - ideal_bmi) / ideal_bmi) * 100)

        # Determine health status
        if 18.5 <= float(bmi) <= 24.9:
            health_status = "You're healthy"
        else:
            health_status = "Cautious"

        # Query to fetch additional health metrics
        cursor.execute("""
            SELECT blood_pressure, heart_rate, blood_sugar, activity_level, sleep_quality, wellness 
            FROM health_metrics 
            WHERE patient_id = %s
        """, (user_id,))
        health_metrics = cursor.fetchone()

        # Explicitly consume the cursor to avoid issues
        cursor.fetchall()


        if not health_metrics:
            # Handle case where no health metrics are found
            return render_template('error.html', message="Health metrics not found")

        # Unpack health metrics
        blood_pressure, heart_rate, blood_sugar, activity_level, sleep_quality, wellness = health_metrics

        # Update the queues for blood sugar, blood pressure, and heart rate
        blood_sugar_queue.append(blood_sugar)
        blood_pressure_queue.append(blood_pressure)
        heart_rate_queue.append(heart_rate)

        # Map activity_level, sleep_quality, and wellness to numeric values
        activity_level_mapping = {"High": 3, "Medium": 2, "Low": 1}
        sleep_quality_mapping = {"Good": 3, "Average": 2, "Poor": 1}
        wellness_mapping = {"Excellent": 4, "Good": 3, "Fair": 2, "Poor": 1}

        # Get numeric values for the metrics
        activity_value = activity_level_mapping.get(activity_level, 0)
        sleep_value = sleep_quality_mapping.get(sleep_quality, 0)
        wellness_value = wellness_mapping.get(wellness, 0)

        # Calculate average and append to the queue
        activity_growth_average = int((activity_value + sleep_value + wellness_value)*10 / 3)
        activity_growth_queue.append(activity_growth_average)

    finally:
        cursor.close()
        connection.close()

    # Render the HTML template with dynamic data
    return render_template(
        'patientpage.html',
        height=height,
        weight=weight,
        bmi=bmi,
        bmi_percentage=bmi_percentage,
        health_status=health_status,
        blood_pressure=blood_pressure,
        heart_rate=heart_rate,
        blood_sugar=blood_sugar,
        activity_level=activity_level,
        sleep_quality=sleep_quality,
        wellness=wellness,
        blood_sugar_list=list(blood_sugar_queue),  # Pass blood sugar queue as a list
        blood_pressure_list=list(blood_pressure_queue),  # Pass blood pressure queue as a list
        heart_rate_list=list(heart_rate_queue),  # Pass heart rate queue as a list
        activity_growth_list=list(activity_growth_queue)  # Pass activity growth queue as a list
    )





# Run the application
if __name__ == '__main__':
    app.run(debug=True)
