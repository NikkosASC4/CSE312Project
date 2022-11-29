import os

from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
#import bcrypt
mongo_client = pymongo.MongoClient("mongo")
db = mongo_client["cse312"]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# def hello_world():
#     """Print 'Hello, world!' as the response body."""
#     return 'Hello, world!'
@app.route('/register', methods=["GET", "POST"])
def register_page():
    return render_template('loginpage.html')

def login():
    userName = request.form['username']
    password = request.form['password']

    if userName not in db:
        return render_template('login.html',info)


if __name__ == "__main__":
    app.run()
