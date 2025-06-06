from flask import Flask, render_template, request, jsonify
from db import execute_query
import traceback
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

 
app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['DEBUG'] = True
 
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'lakshana'


def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

def authenticate_user(username):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()       
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            return user
        else:
            return None

    except Exception as e:
        print("Error in authenticate_user:", str(e))
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def register_user(username, password, email):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE BINARY username = %s OR BINARY email = %s"
            cursor.execute(query, (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                print("User or email already exists:", existing_user)
                return False

            insert_query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (username, password, email))
            connection.commit()

        return True
    except Exception as e:
        print("Error:", str(e))
        return False
    finally:
        connection.close()

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/login_form', methods=['POST'])
def login_form():
    username = request.form['username']
    password = request.form['password']

    user = authenticate_user(username)
    print(user)

    try:
        if user:
            hashed_password = user[2]

            if check_password_hash(hashed_password, password):
                return jsonify({'status': 'success', 'message': 'Login successful'})
            else:
                return jsonify({'status': 'error', 'message': 'Login failed. Incorrect password.'})
        else:
            return jsonify({'status': 'error', 'message': 'Login failed. Please check your credentials.'})
    except Exception as e:
        print("Error:", str(e))
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': 'Login failed. Please try again.'})
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username1']
        password = request.form['password1']
        email = request.form['email']

        hashed_password = generate_password_hash(password)

        try:
            if register_user(username, hashed_password, email):
                return jsonify({'status': 'success', 'message': 'Registration successful'})
            else:
                return jsonify({'status': 'error', 'message': 'Registration failed - Username or email already exists'})
        except Exception as e:
            print("Error:", str(e))
            traceback.print_exc()
            return jsonify({'status': 'error', 'message': 'Registration failed. Please try again.'})

if __name__ == '__main__':
  app.run()