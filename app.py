from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import os
import random
import hashlib

#Declare Database
mongo_client = pymongo.MongoClient("mongo")
db = mongo_client["cse312"]
userAccounts = db["accounts"]
authTokens = db["tokens"]
cartz= db["cart"]

app = Flask(__name__)

#Route declaration
@app.route('/', methods=["GET", "POST"])
def index():
    return redirect(url_for('home_page'))

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
                    response = redirect(url_for('home_page'))
                    token = 'XwQrT' + str(random.randint(0, 1000))
                    hashedToken = hashlib.sha1(token.encode()).digest()
                    authTokens.insert_one({"authtoken": hashedToken, "username": user})
                    response.set_cookie('authToken', token)
                    return response

            else:
                return redirect(url_for('login_page'))
    else:
        return render_template('login.html')


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
      return redirect(url_for('login_page'))
    else:
        return render_template('registration.html')

@app.route('/home', methods=["GET", "POST"])
def home_page():
    return render_template('home.html')

@app.route('/cart', methods=["GET", "POST"])
def cart():
    if request.method == 'POST':
         item = request.form['Item']
         category=request.form['Category']
         price=request.form['Price']
         cartz.insert_one({"Item": item, "Category": category, "Price":price})

         print("HAHAHAHAH")
         print(price)
         return redirect(url_for('cart'))
    else:
        mongoz=cartz.find({})
        carthistory=""
        grandtotal=0
        for p in mongoz:
            carthistory=carthistory+'<div class="layout-inline row th"><div class="col col-pro">'+str(p["Item"])+'</div>'
            carthistory=carthistory+'<div class="col col-price align-center ">'+"$"+str(p["Price"])+'</div>'
            carthistory=carthistory+'<div class="col col-qty align-center">'+str(p["Category"])+'</div><div class="col">'+str(p["Price"])+'</div></div>'
            grandtotal=grandtotal+int(p["Price"])
        carthistory=carthistory+'<div class="layout-inline row th"><div class="col col-pro">'+"Grand Total is"+'</div>'
        carthistory=carthistory+'<div class="col col-price align-center ">'+" "+'</div>'
        carthistory=carthistory+'<div class="col col-qty align-center">'+" "+'</div><div class="col">'+"$"+str(grandtotal)+'</div></div>'
        return render_template('cart.html',carter=carthistory)


@app.route('/settings')
def settings():
    return "hi"

@app.route('/listing', methods=["GET","POST"])
def listing():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f'{key}: {value}')
        return render_template('listing.html')

    else:
        return render_template('listing.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
