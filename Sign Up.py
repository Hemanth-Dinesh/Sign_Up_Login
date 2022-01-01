from flask import Flask,render_template, redirect, url_for,session,request
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb
import smtplib
import uuid
import urllib
from urllib.parse import urlparse
from urllib.parse import parse_qs


app = Flask(__name__)
app.secret_key = "123123"
app.config["MYSQL_Host"] = "127.0.0.1"
app.config["MYSQL_User"] = "root"
app.config["MYSQL_Password"] = "Hemanth1234"
app.config["MYSQL_DB "] = "login"
port = 465
db = MySQL(app)
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            db=mysql.connector.connect(user='root', password='Hemanth1234',
                                       host='127.0.0.1',
                                       database='login')
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT email,password FROM logininfo WHERE email = %s AND password = %s",(username,password))
            info = cursor.fetchone()
            if info is not None and info[0] == username and info[1] == password:
                return render_template("Login Succesful.html")
            else:
                return render_template("Login Unsuccesful.html")
    return render_template("Login2.html")
@app.route('/reset', methods = ['GET','POST'])
def reset():
    if request.method == "POST":
        if 'password' in request.form and 'passResetID' in request.form:
            password = request.form['password']
            uuid = request.form['passResetID']
            db=mysql.connector.connect(user='root', password='Hemanth1234',
                                       host='127.0.0.1',
                                       database='login')
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT uuid FROM logininfo WHERE uuid =%s",(uuid,))
            info = cur.fetchone()
            if info is not None:
                cur.execute("UPDATE logininfo SET password =%s , uuid = null WHERE uuid =%s",(password,uuid))
                db.commit()
                return redirect(url_for('index'))
    if request.method == "GET":
        qs = request.query_string
        str = qs.decode("utf-8")
        keyvalues = str.split('=')
        passreset=keyvalues[1]
        return render_template("PasswordReset.html",passResetID= passreset)






@app.route('/register', methods =  ['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        if "one" in request.form and 'two' in request.form and "three" in request.form:
            name = request.form['one']
            email = request.form['two']
            password = request.form['three']
            db=mysql.connector.connect(user='root', password='Hemanth1234',
                                       host='127.0.0.1',
                                       database='login')
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT email FROM logininfo WHERE email = %s",(email,))
            info = cur.fetchone()
            if info is not None:
                return render_template("Login Unsuccesful.html")
            else:
                cur.execute("INSERT INTO login.logininfo(name, email,password)VALUES(%s,%s,%s ) ",(name,email,password))

                db.commit()
                return redirect(url_for('index'))
    return render_template("Register.html")
@app.route('/forgotpassword', methods = ['GET','POST'])
def forgot_password():
    if request.method == "POST":
        if "email" in request.form:
            email = request.form['email']
            db=mysql.connector.connect(user='root', password='Hemanth1234',
                               host='127.0.0.1',
                               database='login')
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT email FROM logininfo WHERE email = %s",(email,))
            info = cur.fetchone()
            if info is not None:
                passResetID = uuid.uuid4().hex
                resetLink = "Reset Your Password Here: http://127.0.0.1:5000/reset?passResetID=" + passResetID
                cur.execute("UPDATE logininfo SET uuid =%s WHERE email = %s",(passResetID,email))
                db.commit()
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login('plantflask@gmail.com','ORGAIN20')
                message = 'subject: {}\n\n{}' .format('Password Reset',resetLink)
                server.sendmail("plantflask@gmail.com", email, message)
                server.quit()


                return render_template("Login2.html")

            else:
                return redirect(url_for('Login Unsuccesful.html'))


    return render_template("ForgotPassword.html")



if __name__ == '__main__':
    app.run(debug=True)