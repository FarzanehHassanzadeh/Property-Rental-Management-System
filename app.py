from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from user import User

# This initiates the flask application
app = Flask('__name__')

# Connect to MongoDB
client = MongoClient('localhost', 27017)

role = str()


def user_is_tenant():
    role = 'tenant'


def user_is_owner():
    role = 'owner'


@app.route('/', methods=['GET', 'POST'])
def start_page():
    return render_template('start.html')


@app.route('/sign_up')
def signup_page():
    return render_template('signup_page.html')


@app.route('/login', methods=['POST'])
def login_page():
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'], request.form['email'], request.form['birthday'],
                    Role='owner')

    return render_template('html.html')


if __name__ == '__main__':
    app.run(debug=True)
