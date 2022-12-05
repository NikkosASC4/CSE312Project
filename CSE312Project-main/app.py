from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import os

#Declare Database
mongo_client = pymongo.MongoClient("mongo")
db = mongo_client["cse312"]
userAccounts = db["accounts"]

app = Flask(__name__)

#Route declaration
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == 'POST':
      #Retrieve inputs
      user = request.form['username']
      password = (request.form['password']).encode()
      #Validate input with database
      accounts = userAccounts.find({})
      for account in accounts:
          if user in account.get('username'):
              pswrd = account.get('password')
              if bcrypt.checkpw(password, pswrd) == True:
                  return redirect(url_for('home_page'))
              else:
                  return redirect(url_for('index'))
    else:
        return render_template('auth/login.html')


@app.route('/register', methods=["GET", "POST"])
def register_page():
    if request.method == 'POST':
      #Recieve inputs
      user = request.form['username']
      password = (request.form['password']).encode()
      #Salt and hash password
      generatedSalt = bcrypt.gensalt(10)
      password = bcrypt.hashpw(password, generatedSalt)
      #Store username and password in database
      userAccounts.insert_one({"username": user, "password": password})
      return redirect(url_for('index'))
    else:
        return render_template('auth/registration.html')

@app.route('/home', methods=["GET", "POST"])
def home_page():
    return render_template('home.html')


@app.route('/settings')
def settings():
    return "hi"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
