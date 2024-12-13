import datetime
from flask import Flask, render_template, request, redirect, flash, session, url_for
import mysql.connector


#------------------------------------------------------------------------------------------------------------------------------------------------------#


# إنشاء الاتصال بقاعدة البيانات
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Mohamed0159',  # تأكد من تغيير كلمة المرور إذا لزم الأمر
            database='healthcaresystem'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        exit(1)

#------------------------------------------------------------------------------------------------------------------------------------------------------#


# إنشاء تطبيق Flask
app = Flask(__name__, template_folder='.')
app.secret_key = 'your_secret_key'  # مهمة لاستخدام الرسائل عبر flash


#------------------------------------------------------------------------------------------------------------------------------------------------------#


# صفحة تسجيل الدخول
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # التحقق من بيانات المستخدم
        connection = create_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        # check if user exit or no
        if user is None:
            flash('Email or password is incorrect', 'error')
            return render_template('log in.html')
        if email != user[2]:
            flash('Email not exit', 'error')
            return render_template('log in.html')
        elif password != user[3]:
            flash('Password not correct', 'error')
            return render_template('log in.html')
        elif email == user[2] and password == user[3] and user[5].lower() == 'patient':
            flash('Login successful!', 'success')
            return redirect(url_for('لسه هدخله علي الصفحة بتاعته المريض '))###############
        elif email == user[2] and password == user[3] and user[5].lower() == 'doctor':
            flash('Login successful!', 'success')
            return redirect(url_for('لسه هدخله علي الصفحة بتاعته الطبيب '))
        else:
            error = flash('Invalid username or password', 'error')

    return render_template('log in.html', error=error)



#------------------------------------------------------------------------------------------------------------------------------------------------------#


# صفحة اختيار نوع الحساب
@app.route('/which', methods=['GET', 'POST'])
def which():
    if request.method == 'POST':
        account_type  = request.form['account_type']

        if account_type  == 'doctor':
            return redirect(url_for('doctor_profile_signup'))
        elif account_type  == 'patient':
            return redirect(url_for('patient_profile_signup'))
        
    return render_template('Account Type.html')



#------------------------------------------------------------------------------------------------------------------------------------------------------#




@app.route('/doctor_profile_signup', methods=['GET', 'POST'])
def doctor_profile_signup():
    if request.method == 'POST':
        user_name = request.form.get('user_name')  # Use form.get for POST requests
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        phone = request.form.get('phone', '')
        role = 'doctor'
        profile_picture = ''
        gender = request.form.get('gender')
        age = request.form.get('age', 0)

        # التحقق من تطابق كلمة المرور
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('doctor_profile_signup'))

        # التحقق من وجود البريد الإلكتروني في قاعدة البيانات
        connection = create_connection()
        cursor = connection.cursor()
        query_check_email = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already exists! Please log in.', 'danger')
            return redirect(url_for('log in'))  # توجيه المستخدم إلى صفحة تسجيل الدخول

        # إدخال البيانات في قاعدة البيانات
        query = """
            INSERT INTO users (name, email, password, phone, role, profile_picture, gender, age)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_name, email, password, phone, role, profile_picture, gender, age))

        connection.commit()
        cursor.close()
        connection.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('doctor_profile_signup'))  # Redirect to avoid resubmitting the form if the page is refreshed

    return render_template('doctor_profile_signup.html')




#------------------------------------------------------------------------------------------------------------------------------------------------------#



# صفحة تسجيل المريض
@app.route('/patient_profile_signup', methods=['GET', 'POST'])
def patient_profile_signup():
    if request.method == 'POST':
        # الحصول على البيانات المدخلة من المستخدم
        return redirect(url_for('patient_profile_signup'))

    return render_template('Patient_Profile_signup.html')


#------------------------------------------------------------------------------------------------------------------------------------------------------#


# صفحة التسجيل
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['full-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone = request.form.get('phone', '')
        role = 'user'
        profile_picture = ''
        gender = request.form['gender']
        age = request.form.get('age', 0)

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect('/signup')

        connection = create_connection()
        cursor = connection.cursor()

        # التحقق من وجود البريد الإلكتروني
        query_check_email = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email is already registered!', 'danger')
            return redirect('/signup')

        # إدخال بيانات المستخدم الجديد
        query = """
            INSERT INTO users (name, email, password, phone, role, profile_picture, gender, age, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        try:
            cursor.execute(query, (name, email, password, phone, role, profile_picture, gender, age))
            connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect('/')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('signup.html')

@app.route('/doctor-appointment', methods=['GET', 'POST'])
def set_appointment():

    # Check if doctor_id is in the session
    if 'doctor_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if session is missing

    doctor_id = session['doctor_id']  # Retrieve doctor_id from the session

    conn = create_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # Get and type-cast form data
            email=request.form["email"]
            date=request.form['date']  # Expected format: 'YYYY-MM-DD'
            time=request.form['time']  # Expected format: 'HH:MM:SS'
            reason=str(request.form['reason'])  # Ensure reason is a string
            
            # Combine and validate date and time into a `datetime` object
            date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

            email_query = "SELECT user_id FROM users WHERE email = %s AND role = 'Patient'"
            cursor.execute(email_query, (email,))
            result = cursor.fetchone()
            
            if not result:
                return f"No patient found with the email: {email}", 400
            
            # If email exists, retrieve patient_id
            patient_id = int(result[0])
            # Ensure ID are integers
            doctor_id = int(doctor_id)

            # Insert the appointment into the database
            query = """
                INSERT INTO appointments (patient_id,doctor_id,date_time,status,reason)
                VALUES (%s,%s,%s,'Confirmed',%s)
            """
            cursor.execute(query,(patient_id,doctor_id,date_time,reason))
            conn.commit()

            # Retrieve the auto-generated appointment_id
            appointment_id = cursor.lastrowid

            # Close the database connection
            cursor.close()
            return render_template('Appointment Doctor.html',email=email,date=date,time=time,reason=reason)

        except ValueError as ve:
            return f"Invalid data format: {ve}", 400
        except Exception as e:
            return f"An error occurred: {e}", 500

    # Render the form for GET requests
    #return render_template('create_appointment.html')

@app.route("/appointments", methods=["GET"])
def view_appointments():
    # Get patient_id from session
    patient_id = session.get("patient_id")
    if not patient_id:
        return redirect(url_for("login"))  # Redirect to login if not logged in

    # Connect to the database
    connection = create_connection()
    cursor = connection.cursor()
    
    # Query to fetch appointments for the logged-in patient 
    query = """
        SELECT 
            u.name AS patient_username,
            a.date_time,
            a.status,
            a.reason
        FROM appointments AS a
        JOIN users AS u ON a.patient_id = u.user_id
        WHERE a.patient_id = %s
        ORDER BY a.date_time ASC
    """
    cursor.execute(query, (patient_id,))
    appointments = cursor.fetchall()
    
    # Close the connection
    cursor.close()
    connection.close()

    # Separate the results into different lists
    date = [appointment['date_time'].strftime('%m/%d/%Y') for appointment in appointments]
    time = [appointment['date_time'].strftime('%I:%M %p') for appointment in appointments]
    reason = [appointment['reason'] for appointment in appointments]

    # Pass these separate values to the HTML template
    return render_template("Appointment of patient.html",
                           date=date,
                           time=time,
                           reason=reason)


@app.route('/add-medication', methods=['POST'])
def add_medication():
    try:
        # Get the current doctor's ID from the session
        if 'doctor_id' not in session:
            flash("Unauthorized access. Please log in as a doctor.", "danger")
            return redirect(url_for('login'))  # Redirect to login page if not logged in

        doctor_id = session['doctor_id']

        # Query to get the first 5 related patients for the current doctor with appointment details
        conn = create_connection()
        cursor = conn.cursor()
        patient_query = """
            SELECT u.patient_id, u.name, u.date_of_birth, a.reason, a.date_time 
            FROM users u
            JOIN appointments a ON u.patient_id = a.patient_id
            WHERE a.doctor_id = %s
            ORDER BY a.date_time ASC
            LIMIT 5
        """
        cursor.execute(patient_query, (doctor_id,))
        related_patients = cursor.fetchall()

        # Assign each patient to a separate variable
        # Retrieve form data
        medication_name = request.form['medication_name'].strip()
        dosage = request.form['dosage'].strip()
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        instructions = request.form['instructions'].strip()
        patient_id = request.get_json().get('patient_id')

        # Validate dates
        if end_date < start_date:
            flash("End date cannot be earlier than start date.", "danger")
            return render_template('new_med.html',patients=related_patients)

        # Insert medication into the database
        medication_query = """
            INSERT INTO medications (patient_id, doctor_id, medication_name, dosage, start_date, end_date, instructions)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (patient_id, doctor_id, medication_name, dosage, start_date, end_date, instructions)
        cursor.execute(medication_query, values)
        conn.commit()

        flash("Medication added successfully!", "success")
        return render_template('medication.html', patients=related_patients)

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('health_monitoring'))
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route("/patient-medications", methods=["GET"])
def medication_details():
    # Get patient_id from the session
    patient_id = session.get("patient_id")
    if not patient_id:
        return redirect(url_for("login"))  # Redirect to login if not logged in

    # Connect to the database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query to join medications and users tables
    query = """
        SELECT 
            m.medication_name, 
            m.dosage, 
            u.name AS doctor_name, 
            m.start_date, 
            m.end_date, 
            m.instructions
        FROM medications AS m
        JOIN users AS u ON m.doctor_id = u.user_id
        WHERE m.patient_id = %s
    """
    cursor.execute(query, (patient_id,))
    medications = cursor.fetchall()
    
    # Separate data into individual variables
    medication_name=[med["medication_name"] for med in medications]
    dosage =[med["dosage"] for med in medications]
    doctor_name=[med["doctor_name"] for med in medications]
    start_date=[med["start_date"] for med in medications]
    end_date=[med["end_date"] for med in medications]
    instruction=[med["instructions"] for med in medications]
    
    # Close the connection
    cursor.close()
    connection.close()
    
    # Pass separated data to the HTML template
    return render_template(
        "medication_patient.html", 
        medication_name=medication_name,
        dosage=dosage,
        doctor_name=doctor_name,
        start_date=start_date,
        end_date=end_date,
        instruction=instruction
    )
#------------------------------------------------------------------------------------------------------------------------------------------------------#



# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)


