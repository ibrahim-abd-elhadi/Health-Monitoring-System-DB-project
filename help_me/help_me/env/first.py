from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector
import logging

# Database Connection Function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='yY7$ls44',  # Update your MySQL password here
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
            return redirect(url_for('patient_details'))
        elif user[5].lower() == 'doctor':
            flash('Login successful!', 'success')
            session['user_id'] = user[0]  # Assuming `user[0]` is `user_id`
            return redirect(url_for('patient_profile'))
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
        date_of_birth = request.form.get('date_of_birth')
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
            INSERT INTO users (name, email, password, phone, role, gender, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_name, email, password, phone, role, gender, date_of_birth))

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
        date_of_birth = request.form.get('date_of_birth')
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
            INSERT INTO users (name, email, password, phone, role, gender, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """


        cursor.execute(query, (user_name, email, password, phone, role, gender, date_of_birth))

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
        blood_type = request.form['blood_type']
        chronic_conditions = request.form.get('chronic_conditions', '')
        emergency_contact = request.form.get('emergency_contact', '')
        

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
                patient_data = (user_id, height, weight, blood_type, chronic_conditions, emergency_contact)

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
@app.route('/index')
def index():
    return render_template('index.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route("/patient_profile", methods=['GET', 'DELETE'])
def patient_profile():
    doctor_id = session.get('user_id', None)
    # return render_template("test.html", doctor_id=doctor_id)
    if doctor_id is None:
        flash('User is not logged in!', 'danger')
        return redirect(url_for('login'))
    
    
    connection = create_connection()
    cursor = connection.cursor()


    # check if user exists and is a doctor
    query = "SELECT * FROM users WHERE user_id = %s AND role = 'doctor'"
    cursor.execute(query, (doctor_id,))
    if cursor.fetchone() is None:
        flash('Access denied!', 'warning')
        return redirect(url_for('login'))

    if request.method == 'DELETE':
        query = "DELETE FROM appointments WHERE patient_id = %s"
        cursor.execute(query, (request.get_json().get('patient_id'),))
        connection.commit()
        return redirect(url_for('patient_profile'))
    
    

    query_last_doctor_id = """ SELECT appointments.reason, appointments.status,
    appointments.date_time, users.name, users.user_id, users.profile_picture
    FROM appointments LEFT JOIN users ON appointments.patient_id=users.user_id WHERE doctor_id = %s;"""
    
    # Pass doctor_id as a tuple with a single element
    cursor.execute(query_last_doctor_id, (doctor_id,))
    patients = cursor.fetchall()  # Fetch the single result
    
    cursor.close()
    connection.close()
    
    if patients is None:
        flash('User not found!', 'warning')
        return redirect(url_for('login'))
    
    return render_template('patient_profile.html', patients=patients)



@app.route("/update_patient_profile", methods=['GET', 'POST'])
def update_patient_profile():
    user_id = session.get('user_id', None)
    if user_id is None:
        flash('User is not logged in!', 'danger')
        return redirect(url_for('login'))


    connection = create_connection()
    cursor = connection.cursor()

    # check if user exists and is a patient
    query = "SELECT * FROM users WHERE user_id = %s AND role = 'patient'"
    cursor.execute(query, (user_id,))
    if cursor.fetchone() is None:
        flash('Access denied!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                # Save the file or process it
                photo_name = photo.filename  # Example path
                photo.save(f"static/uploads/{photo_name}")
                query = "UPDATE users SET profile_picture = %s WHERE user_id = %s"
                cursor.execute(query, (photo_name, user_id))
                connection.commit()
        else:
            name = request.form['name']
            phone = request.form['phone']
            weight = request.form['weight']
            chronic_conditions = request.form['chronic_conditions']

        
        try:

            if name:
                query = "UPDATE users SET name = %s WHERE user_id = %s"
                cursor.execute(query, (name, user_id))
                connection.commit()

            if phone:
                query = "UPDATE users SET phone = %s WHERE user_id = %s"
                cursor.execute(query, (phone, user_id))
                connection.commit()

            if weight:
                query = "UPDATE patients SET weight = %s WHERE patient_id = %s"
                cursor.execute(query, (weight, user_id))
                connection.commit()

            if chronic_conditions:
                query = "UPDATE patients SET chronic_conditions = %s WHERE patient_id = %s"
                cursor.execute(query, (chronic_conditions, user_id))
                connection.commit()


            flash('Profile updated successfully!', 'success')
            return redirect(url_for('update_patient_profile'))

        except Exception as e:
            logging.error(f"Error updating user: {e}")
            flash('An error occurred while updating your profile. Please try again.', 'danger')

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            flash('Profile updated successfully!', 'success')
    

    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = "SELECT name, phone FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        name, phone = cursor.fetchone()
        query = "SELECT weight, chronic_conditions FROM patients WHERE patient_id = %s"
        cursor.execute(query, (user_id,))
        weight, chronic_conditions = cursor.fetchone()

    except Exception as e:
        logging.error(f"Error fetching user information: {e}")
        flash('An error occurred while loading your profile settings.', 'danger')
        return redirect(url_for('update_doctor_profile'))

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    
    return render_template('patient_update_profile.html', name=name, phone=phone, weight=weight, chronic_conditions=chronic_conditions)

@app.route("/update_doctor_profile", methods=['GET', 'POST'])
def update_doctor_profile():
    user_id = session.get('user_id', None)
    if user_id is None:
        flash('User is not logged in!', 'danger')
        return redirect(url_for('login'))


    connection = create_connection()
    cursor = connection.cursor()

    # check if user exists and is a doctor
    query = "SELECT * FROM users WHERE user_id = %s AND role = 'doctor'"
    cursor.execute(query, (user_id,))
    if cursor.fetchone() is None:
        flash('Access denied!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                # Save the file or process it
                photo_name = photo.filename  # Example path
                photo.save(f"static/uploads/{photo_name}")
                query = "UPDATE users SET profile_picture = %s WHERE user_id = %s"
                cursor.execute(query, (photo_name, user_id))
                connection.commit()
        else:
            name = request.form['doctor_name']
            phone = request.form['phone']
            hospital_affiliation = request.form['hospital_affiliation']

        
        try:

            if name:
                query = "UPDATE users SET name = %s WHERE user_id = %s"
                cursor.execute(query, (name, user_id))
                connection.commit()

            if phone:
                query = "UPDATE users SET phone = %s WHERE user_id = %s"
                cursor.execute(query, (phone, user_id))
                connection.commit()

            if hospital_affiliation:
                query = "UPDATE doctors SET hospital_affiliation = %s WHERE doctor_id = %s"
                cursor.execute(query, (hospital_affiliation, user_id))
                connection.commit()


            flash('Profile updated successfully!', 'success')
            return redirect(url_for('update_doctor_profile'))

        except Exception as e:
            logging.error(f"Error updating user: {e}")
            flash('An error occurred while updating your profile. Please try again.', 'danger')

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            flash('Profile updated successfully!', 'success')
    

    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = "SELECT name, phone FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        name, phone = cursor.fetchone()
        query = "SELECT hospital_affiliation FROM doctors WHERE doctor_id = %s"
        cursor.execute(query, (user_id,))
        hospital_affiliation = cursor.fetchone()[0]

    except Exception as e:
        logging.error(f"Error fetching user information: {e}")
        flash('An error occurred while loading your profile settings.', 'danger')
        return redirect(url_for('update_doctor_profile'))

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    
    return render_template('doctor_update_profile.html', name=name, phone=phone, hospital_affiliation=hospital_affiliation)




@app.route("/change_password_patient", methods=['GET', 'POST']) 
def change_password_patient():

    user_id = session.get('user_id', None)
    if user_id is None:
        flash('User is not logged in!', 'danger')
        return redirect(url_for('login'))


    connection = create_connection()
    cursor = connection.cursor()

    # check if user exists and is a patient
    query = "SELECT * FROM users WHERE user_id = %s AND role = 'patient'"
    cursor.execute(query, (user_id,))
    
    if cursor.fetchone() is None:
        flash('Access denied!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form['current-password']
        new_password = request.form['new-password']
        confirm_new_password = request.form['confirm-new-password']

        if new_password != confirm_new_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('change_password_patient'))

        try:
            query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
            cursor.execute(query, (user_id, current_password))
            if cursor.fetchone() is None:
                flash('Old password is incorrect!', 'danger')
                return redirect(url_for('change_password_patient'))

            query = "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(query, (new_password, user_id))
            connection.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('which'))

        except Exception as e:
            logging.error(f"Error updating password: {e}")
            flash('An error occurred while updating your password. Please try again.', 'danger')

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return render_template('change_password_patient.html')


@app.route("/change_password_doctor", methods=['GET', 'POST']) 
def change_password_doctor():

    user_id = session.get('user_id', None)
    if user_id is None:
        flash('User is not logged in!', 'danger')
        return redirect(url_for('login'))


    connection = create_connection()
    cursor = connection.cursor()

    # check if user exists and is a doctor
    query = "SELECT * FROM users WHERE user_id = %s AND role = 'doctor'"
    cursor.execute(query, (user_id,))
    
    if cursor.fetchone() is None:
        flash('Access denied!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form['current-password']
        new_password = request.form['new-password']
        confirm_new_password = request.form['confirm-new-password']

        if new_password != confirm_new_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('change_password_doctor'))

        try:
            query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
            cursor.execute(query, (user_id, current_password))
            if cursor.fetchone() is None:
                flash('Old password is incorrect!', 'danger')
                return redirect(url_for('change_password_doctor'))

            query = "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(query, (new_password, user_id))
            connection.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('patient_profile'))

        except Exception as e:
            logging.error(f"Error updating password: {e}")
            flash('An error occurred while updating your password. Please try again.', 'danger')

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return render_template('change_password_doctor.html')