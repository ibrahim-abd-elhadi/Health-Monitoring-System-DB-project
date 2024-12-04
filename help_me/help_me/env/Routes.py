from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__,template_folder=os.path.join(os.path.dirname(__file__), "env", "template"))
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

DATABASE = 'HealthcareSystem.db'  # Path to your SQLite database



def get_db_connection():
    """Helper function to connect to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries for easier access
    return conn


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':  # If the form was submitted
        username = request.form['username']
        password = request.form['password']

        # Connect to the database and validate credentials
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:  # If the user exists and credentials match
            flash('Login successful!')
            return redirect(url_for('index'))  # Redirect to the home page
        else:  # If the credentials are incorrect
            error = 'Invalid username or password'
            return render_template('login.html', error=error)  # Re-render login page with error

    return render_template('login.html')  # Render login page when first accessing the page (GET)


@app.route('/account_type')
def account_type():
    return "Account Type Page"  # Replace with the actual account type selection template



#signup for doctors
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the data from the form
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        address = request.form.get('address')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        user_type = request.form.get('user_type')  # Identify if the user is a doctor or patient

        # Check if all fields are filled
        if not all([full_name, username, email, password, confirm_password, address, dob, gender, user_type]):
            flash("All fields are required!", "error")
            return redirect(url_for('signup'))

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup'))

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username or email already exists. Please choose another one.", "error")
            return redirect(url_for('signup'))

        # Insert the new user into the users table
        cursor.execute("""
            INSERT INTO users (full_name, username, email, password, address, dob, gender, user_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name, username, email, password, address, dob, gender, user_type))
        conn.commit()

        # Get the user ID of the newly inserted user
        user_id = cursor.lastrowid

        conn.close()

        # Redirect to the doctor profile page if the user is a doctor
        if user_type == 'doctor':
            return redirect(url_for('doctor_profile', user_id=user_id))

        # Otherwise, redirect to the login page
        flash("Signup successful!", "success")
        return redirect(url_for('login'))

    # If it's a GET request, render the signup page
    return render_template('signup.html')

@app.route('/doctor_profile/<int:user_id>', methods=['GET', 'POST'])
def doctor_profile(user_id):
    if request.method == 'POST':
        # Get the specialization and license number from the form
        specialization = request.form.get('specialization')
        license_number = request.form.get('license_number')

        if not all([specialization, license_number]):
            flash("All fields are required!", "error")
            return redirect(url_for('doctor_profile', user_id=user_id))

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the doctor-specific data into the doctor table
        cursor.execute("""
            INSERT INTO doctor (user_id, specialization, license_number)
            VALUES (?, ?, ?)
        """, (user_id, specialization, license_number))
        conn.commit()
        conn.close()

        # Flash success message and redirect to login
        flash("Doctor profile completed successfully!", "success")
        return redirect(url_for('login'))

    # Render the doctor profile page for GET requests
    return render_template('doctor_profile.html', user_id=user_id)






@app.route('/signup_patient', methods=['GET', 'POST'])
def signup_patient():
    if request.method == 'POST':
        # Get the data from the form
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        address = request.form.get('address')
        dob = request.form.get('dob')
        gender = request.form.get('gender')

        # Check if all fields are filled
        if not all([full_name, username, email, password, confirm_password, address, dob, gender]):
            flash("All fields are required!", "error")
            return redirect(url_for('signup_patient'))

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup_patient'))

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username or email already exists. Please choose another one.", "error")
            return redirect(url_for('signup_patient'))

        # Insert the new user into the users table
        cursor.execute("""
            INSERT INTO users (full_name, username, email, password, address, dob, gender, user_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'patient')
        """, (full_name, username, email, password, address, dob, gender))
        conn.commit()

        # Get the user ID of the newly inserted user
        user_id = cursor.lastrowid

        conn.close()

        # Redirect to the patient profile page
        return redirect(url_for('patient_profile', user_id=user_id))

    # If it's a GET request, render the signup_patient page
    return render_template('signup_patient.html')


@app.route('/patient_profile/<int:user_id>', methods=['GET', 'POST'])
def patient_profile(user_id):
    if request.method == 'POST':
        # Get patient-specific data from the form
        height = request.form.get('height')
        weight = request.form.get('weight')
        blood_type = request.form.get('blood_type')
        chronic_conditions = request.form.get('chronic_conditions')
        emergency_contact = request.form.get('emergency_contact')

        # Check if all fields are filled
        if not all([height, weight, blood_type, chronic_conditions, emergency_contact]):
            flash("All fields are required!", "error")
            return redirect(url_for('patient_profile', user_id=user_id))

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the patient-specific data into the patient table
        cursor.execute("""
            INSERT INTO patient (user_id, height, weight, blood_type, chronic_conditions, emergency_contact)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, height, weight, blood_type, chronic_conditions, emergency_contact))
        conn.commit()
        conn.close()

        # Flash success message and redirect to login
        flash("Patient profile completed successfully!", "success")
        return redirect(url_for('login'))

    # Render the patient profile page for GET requests
    return render_template('patient_profile.html', user_id=user_id)


###############
##33333
#نااااااااااااقص
@app.route('/dashboard')
def dashboard():
    # Example dynamic data to pass to the template
    appointments_count = 2
    activity_percentage = 25
    sleep_percentage = 79
    wellness_percentage = 52
    activity_offset = 211.575
    sleep_offset = 59.823
    wellness_offset = 135.72
    statuses = [
        {'name': 'Rabies', 'status': 'In danger', 'class': 'danger', 'date': '01 Dec 2023', 'action': 'Call Emergency'},
        {'name': 'Bordetella', 'status': 'Abnormal', 'class': 'alert', 'date': '11 Dec 2024', 'action': 'Alert'},
        {'name': 'Distemper', 'status': 'Normal', 'class': 'normal', 'date': '27 Jun 2024', 'action': 'Chat'},
    ]
    chats = [
        {'name': 'Helen Brooks', 'message': 'Luna has been scratching her ears...'},
        {'name': 'Kathryn Murphy', 'message': 'The best way to treat an ear infection...'},
        {'name': 'James Grey', 'message': 'You should follow the instructions...'},
        {'name': 'Jim Brown', 'message': 'Hi, I have a question about my cat.'},
    ]

    return render_template('index.html', appointments_count=appointments_count, activity_percentage=activity_percentage, sleep_percentage=sleep_percentage, wellness_percentage=wellness_percentage, activity_offset=activity_offset, sleep_offset=sleep_offset, wellness_offset=wellness_offset, statuses=statuses, chats=chats)









if __name__ == '__main__':
    app.run(debug=True)




