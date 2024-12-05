from flask import Flask, render_template, request, redirect, flash, url_for
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



#------------------------------------------------------------------------------------------------------------------------------------------------------#



# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)


