from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from user import User
import re
from datetime import datetime


# Validation functions
# Check the passwork if it is at least 8 characters and has capital, small letters, special characters and numbers
def validate_password(password):
    password_pattern = (
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
    )
    return re.match(password_pattern, password) is not None


# Check of the email is in the correct format. It must end with @gmail.com or @email.com
def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|email\.com)$'
    return re.match(email_pattern, email) is not None


def validate_birthday(birthday):
    # Check if the birthday is in the correct format YYYY-MM-DD
    try:
        # Attempt to parse the date using datetime
        datetime.strptime(birthday, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# This initiates the flask application
app = Flask('__name__')

# Connect to MongoDB
client = MongoClient('localhost', 27017)


@app.route('/', methods=['GET', 'POST'])
def start_page():
    return render_template('start.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login_stat = "owner_login"
    if request.method == 'POST':
        username_owner_input = request.form.get("username-owner")
        email_owner_input = request.form.get("email-owner")
        password_owner_input = request.form.get("password-owner")

        username_tenant_input = request.form.get("username-tenant")
        email_tenant_input = request.form.get("email-tenant")
        password_tenant_input = request.form.get("password-tenant")

        login_stat = request.form.get("login_status")
        if login_stat == "owner_login":
            user_record = users_data.find_one({'username': username_owner_input,
                                               'email': email_owner_input,
                                               'password': password_owner_input,
                                               'role': 'owner'})

            if user_record:
                return redirect(url_for('home_page'))
            else:
                return render_template('login.html', login_status=login_stat)

        elif login_stat == "tenant_login":
            user_record = users_data.find_one({'username': username_tenant_input,
                                               'email': email_tenant_input,
                                               'password': password_tenant_input,
                                               'role': 'tenant'})

            if user_record:
                return redirect(url_for('home_page'))
            else:
                return render_template('login.html', login_status=login_stat)

    return render_template('login.html', login_status=login_stat)


@app.route('/signup', methods=['POST', 'GET'])
def signup_page():
    if request.method == 'POST':

        if ((not validate_password(request.form['password'])) or
                (not validate_email(request.form['email']))
                or (not validate_birthday(request.form['birthday']))):
            # The password or email is not in a valid format.
            return render_template('signup.html')

        if (users_data.find_one({'username': request.form['username'], 'role': 'owner'})
                or users_data.find_one({'email': request.form['email'], 'role': 'owner'})):
            # This username or user has already existed, so you can't create another account again.
            return render_template('signup.html')

        user = User(request.form['username'], request.form['password'], request.form['email'], request.form['birthday'],
                    Role='owner')
        d = dict()
        d = user.__dict__
        users_data.insert_one(d)
        return redirect(url_for('home_page'))

    return render_template('signup.html')


@app.route('/signup2', methods=['POST', 'GET'])
def signup_page2():
    if request.method == 'POST':

        if ((not validate_password(request.form['password'])) or
                (not validate_email(request.form['email']))
                or (not validate_birthday(request.form['birthday']))):
            # The password or email is not in a valid format.
            return render_template('signup2.html')

        if (users_data.find_one({'username': request.form['username'], 'role': 'tenant'})
                or users_data.find_one({'email': request.form['email'], 'role': 'tenant'})):
            # This username or user has already existed, so you can't create another account again.
            return render_template('signup2.html')

        user = User(request.form['username'], request.form['password'], request.form['email'], request.form['birthday'],
                    Role='tenant')

        d = dict()
        d = user.__dict__
        users_data.insert_one(d)
        return redirect(url_for('home_page'))

    return render_template('signup2.html')


@app.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


db = client['Property_data']

users_data = db['users_data']

if __name__ == '__main__':
    app.run(debug=True)
