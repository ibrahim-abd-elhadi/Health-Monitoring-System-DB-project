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



connect = create_connection()

cursor = connect.cursor()



cursor.execute("SELECT * FROM users")
user=cursor.fetchone()

print(user)
print(user[3])
print(user[5])











