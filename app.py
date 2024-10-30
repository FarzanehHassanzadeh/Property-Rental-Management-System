from flask import Flask, render_template, request, redirect, url_for

from pymongo import MongoClient
from user import User

# This initiates the flask application
app = Flask('__name__')

# Connect to MongoDB
client = MongoClient('localhost', 27017)


@app.route('/', methods=['GET', 'POST'])
def start_page():
    return render_template('start.html')


@app.route('/sign_up', methods=['POST', 'GET'])
def signup_page():
    return render_template('signup_page.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'], request.form['email'], request.form['birthday'],
                    Role='owner')
        d = dict()
        d = user.__dict__
        users_data.insert_one(d)
        return redirect(url_for('login_page'))

    return render_template('html.html')


@app.route('/login2', methods=['GET', 'POST'])
def login_page2():
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'], request.form['email'], request.form['birthday'],
                    Role='tenant')

        d = dict()
        d = user.__dict__
        users_data.insert_one(d)
        return redirect(url_for('login_page2'))

    return render_template('html2.html')


@app.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


db = client['Property_data']

users_data = db['users_data']

if __name__ == '__main__':
    app.run(debug=True)
