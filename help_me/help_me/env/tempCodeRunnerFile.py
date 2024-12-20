from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector

# Database Connection Function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Saher1234$',  # Update your MySQL password here
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
            return redirect(url_for('patient_details'))
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
        return redirect(url_for('login'))

    return render_template('doctor_profile_signup.html')

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
        emergency_contacts = request.form.getlist('emergency-contacts')
        emergency_contacts_str = ','.join(emergency_contacts)

        connection = create_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO patients (patient_id, height, weight, blood_type, chronic_conditions, emergency_contacts)
            VALUES (%s, %s, %s, NULL, %s, %s)
        """
        cursor.execute(query, (user_id, height, weight, health_history, emergency_contacts_str))

        connection.commit()
        cursor.close()
        connection.close()

        flash('Patient details saved successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('patient_details.html', user_id=user_id)

## Home Page
@app.route('/index')
def index():
    return render_template('index.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
