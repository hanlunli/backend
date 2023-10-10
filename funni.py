from flask import Flask
from flask import render_template, url_for, flash, request, redirect, Response
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm
import os

app = Flask(__name__)
app.debug=True

login_manager = LoginManager(app)
login_manager.login_view = "login"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class User(UserMixin):
    def __init__(self, id, email, password):
         self.id = str(id)
         self.email = email
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id
@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('login.db')
   curs = conn.cursor()
   curs.execute("SELECT * from login where user_id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])

@app.route("/")
def home():
    return redirect("/login")
    
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")
    
@app.route("/register")
def register():
    return render_template("register.html")
    
    
@app.route("/registerAcc", methods=['GET', 'POST'])
def registerAcc():

    userEmail = request.form['email']
    userPassword = request.form['password']

    addDB = "INSERT INTO login(email, password) VALUES(" + "'" + userEmail + "'" + ",'" + userPassword + "')"
    
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()
    cursor.execute(addDB)
    conn.commit()
    conn.close()
    
    return redirect("/login")
    
@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('profile'))
  form = LoginForm()
  if form.validate_on_submit():
     conn = sqlite3.connect('login.db')
     curs = conn.cursor()
     curs.execute("SELECT * FROM login where email = (?)",    [form.email.data])
     user = list(curs.fetchone())
     Us = load_user(user[0])
     if form.email.data == Us.email and form.password.data == Us.password:
        login_user(Us, remember=form.remember.data)
        Umail = list({form.email.data})[0].split('@')[0]
        flash('Logged in successfully '+Umail)
        return redirect('/profile')
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)
if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080,threaded=True)
