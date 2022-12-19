from flask import Flask, render_template,session, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
db = yaml.load(open('db.yaml'), Loader=yaml.Loader)
#Configure DB
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.secret_key = "super secret key"
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    msg=''
    if request.method=='POST':
        EMAIL = request.form['email']
        PASSWORD = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE EMAIL=%s AND PASSWORD=%s",(EMAIL,PASSWORD))
        record = cur.fetchone()
        if record:
            session['loggedin'] = True
            session['email'] = record[1]
            return redirect('/home')
        else:
            msg ='Incorrect passsword/email.Try again!'
    return render_template('index.html', msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #Fetch form data
        f = 0
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM USERS")
        record = cur.fetchall()
        for row in record:
            if password == ''.join(row) or password == '':
                msg = "Password Same or Password Field Can't Be Empty"
                f = 1
                return render_template('register.html', msg=msg)
        if f==0:
            cur.execute("INSERT INTO USERS(name, email, password) VALUES (%s, %s, %s)",(name, email, password))
            mysql.connection.commit()
            cur.close()
            session['email'] = email
            return redirect('/home')
            
    return render_template('register.html')
@app.route('/home')
def home():
    return render_template('home.html',username=session['email'])

@app.route('/logout')
def logout():
    session.pop('logedin',None)
    session.pop('email',None)
    return redirect("/")


if __name__=='__main__':
    app.run(debug=True) 