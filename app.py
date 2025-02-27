from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydatabase'

# Initialize MySQL
mysql = MySQL(app)

# Main route
@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to login page

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash('Incorrect username or password!', 'danger')
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            flash('Username already exists!', 'danger')
        else:
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            reset_link = url_for('reset_password', email=email, _external=True)
            send_reset_email(email, reset_link)
            flash('Password reset link has been sent to your email!', 'success')
        else:
            flash('Email does not exist!', 'danger')
    return render_template('fpassword.html')

@app.route('/index')
def index():
    return render_template("index.html")

# Function to send password reset email
def send_reset_email(email, reset_link):
    sender_email = "your_email@example.com"
    receiver_email = email
    password = "your_email_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Your Password"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Hi,\nPlease click the following link to reset your password:\n{reset_link}"
    html = f"<html><body><p>Hi,<br>Click the link below to reset your password:<br><a href='{reset_link}'>Reset Password</a></p></body></html>"
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

@app.route('/schedule')
def schedule():
    return render_template("schedule.html")

if __name__ == '__main__':
    app.run(debug=True)
