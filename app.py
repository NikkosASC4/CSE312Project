from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import os
import random
import hashlib
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# Declare Database

# from flask_login import LoginManager, UserMixin, login_required, login_user

# Declare Database

mongo_client = pymongo.MongoClient("mongo")
db = mongo_client["cse312"]
userAccounts = db["accounts"]
authTokens = db["tokens"]

cartz = db["cartloz"]
listings = db["listerlolz"]

app = Flask(__name__)


# login_manager = LoginManager()
# login_manager.init_app(app)


# sock = Sock(app)

# Route declaration
@app.route('/', methods=["GET", "POST"])
def index():
    return redirect(url_for('home_page'))


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == 'POST':
        # Retrieve inputs
        user = request.form['username']
        password = (request.form['password']).encode()
        # Validate input with database
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
        # Recieve inputs
        user = request.form['username']
        password = (request.form['password']).encode()
        # Salt and hash password
        generatedSalt = bcrypt.gensalt(10)
        password = bcrypt.hashpw(password, generatedSalt)
        # Store username and password in database
        userAccounts.insert_one({"username": user, "password": password})
        return redirect(url_for('login_page'))
    else:
        return render_template('registration.html')


@app.route('/home', methods=["GET", "POST"])
def home_page():
    return render_template('home.html')


@app.route('/buy', methods=["GET", "POST"])
def buy():
    buystuff = ""
    lister = listings.find({})
    itemlist = ""

    for p in lister:
        itemlist = itemlist + '<div class="item-listing"><form method="post" action="/cart" ' \
                              'enctype="multipart/form-data"><img src="../static/image/pc.jpeg' +'" alt="Insert Alt Text" style="width:100%;height:300px"> <p class="name">' + str(
            p["Name"]) + '</p>' + '<p class="price">' + str(
            p["Price"]) + '</p>' + '<input id="item-name" name="item-name" type="hidden" value="' + str(
            p["Name"]) + '"/>' + '<input name="item-price" id="item-price" type="hidden" value="' + str(
            p["Price"]) + '"\>' + '<input id="item-desc" name="item-desc"type="hidden" value="' + str(
            p["Discription"]) + '"\>' + '<input type="submit" value="Buy"/></form></div>'
    return render_template('buy.html', shop=itemlist)


@app.route('/cart', methods=["GET", "POST"])
def cart():
    if request.method == 'POST':
        Name = request.form['item-name']
        Discription = request.form['item-desc']
        price = request.form['item-price']
        cartz.insert_one({"Item": Name, "Discription": Discription, "Price": price})

        print("HAHAHAHAH")
        print(price)
        return redirect(url_for('buy'))

    else:
        mongoz = cartz.find({})
        carthistory = ""
        grandtotal = 0
        for p in mongoz:
            carthistory = carthistory + '<tr><td>' + str(p["Item"]) + '</td>'
            carthistory = carthistory + '<td>' + "$" + str(p["Price"]) + '</td>'
            carthistory = carthistory + '<td>' + str(p["Discription"]) + '</td><td>' + "$" + str(
                p["Price"]) + '</td></tr>'
            grandtotal = grandtotal + int(p["Price"])
        carthistory = carthistory + '<tr><td>' + "Grand Total is" + '</td>'
        carthistory = carthistory + '<td></td><td></td>'
        carthistory = carthistory + '<td>' + "$" + str(grandtotal) + '</td></tr>'
        return render_template('cart.html', carter=carthistory)


# # Create a class that represents a user
# class User(UserMixin):
#     def __init__(self, username, password_hash):
#         self.username = username
#         self.password_hash = password_hash
#
#
# @login_manager.user_loader
# def load_user(username):
#     # Retrieve the user's information from the database
#     user = db.userAccounts.find_one({'username': username})
#
#     if user:
#         # Create a user object
#         return User(user['username'], user['password'])
#     else:
#         # Return None if the user does not exist
#         return None


@app.route('/profile', methods=["GET", "POST"])
# @login_required
def profile():
    # Get the logged-in user's username from the session
    return render_template('profile.html')


@app.route('/settings', methods=['POST', 'GET'])
# @login_required
def settings():
    if request.method == 'POST':
        # Get the new username and password from the request
        new_username = request.form['username']
        new_password = (request.form['password']).encode()
        # Validate input with database
        # Get the current user's information from the database

        user = userAccounts.find_one({'username': request.form['username']})
        user['username'] = new_username
        generatedSalt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(new_password, generatedSalt)
        userAccounts.update_one({'username': request.form['username']},
                                {'$set': {'username': new_username, 'password': hashed_password}})
        return redirect(url_for('home_page'))
    else:
        return render_template('settings.html')

    # Check if the current user is the owner of the data
    # if current_user['username'] == request.form['username']:
    # Get the user's information from the database

    # else:
    #     return "You are not authorized to edit this user's data!"


@app.route('/listing', methods=["GET", "POST"])
def listing():
    if request.method == 'POST':
        Name = request.form['item-name']
        Discription = request.form['item-desc']
        price = request.form['item-price']
        file = request.files['file'].read()
        listings.insert_one({"Name": Name, "Price": price, "Discription": Discription, "image": file})

        return redirect(url_for('buy'))

    else:
        # cursor = listings.find({})
        print("test fire")
        print(listings)
        for document in listings.find({}, {'_id': False}):
            print(document)
        return render_template('listing.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
