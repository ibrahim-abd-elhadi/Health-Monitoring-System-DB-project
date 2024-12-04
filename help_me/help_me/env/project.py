from flask import Flask, render_template, request, url_for, redirect, flash
import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Saher1234$',
            database='healthcaresystem'
        )
        print("Database connection established.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        exit(1)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Important for using flash messages

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = create_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            flash('Login successful!')
            return redirect(url_for('Account_Type.html'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/index')
def index():
    return "Welcome to the home page!"

@app.route("/sign_up/<user_type>", methods=["GET"])
def sign_up(user_type):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(f"{user_type}_Profile_signup.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
