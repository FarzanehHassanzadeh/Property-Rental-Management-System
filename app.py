from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from user import User
import re
from datetime import datetime
from bson.objectid import ObjectId
import secrets  # Import secrets module for generating a secure secret key

global_fullname = ''
a=''
# Validation functions
# Check the password if it is at least 8 characters and has capital, small letters, special characters and numbers
def validate_password(password):
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
    return re.match(password_pattern, password) is not None

# Check if the email is in the correct format. It must end with @gmail.com or @email.com
def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|email\.com)$'
    return re.match(email_pattern, email) is not None

def validate_birthday(birthday):
    # Check if the birthday is in the correct format YYYY-MM-DD
    try:
        datetime.strptime(birthday, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# This initiates the Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Set a unique and secure secret key

# Connect to MongoDB
client = MongoClient('localhost', 27017)

# Create a database called Property_data
db = client['Property_data']

# Create collections
users_data = db['users_data']
property_owner_data = db['property_owner_data']
cards_data = db['Cards_data']

# This function is used for the start page
@app.route('/', methods=['GET', 'POST'])
def start_page():
    return render_template('start.html')

# ******************************************************
# This Function is used for login page
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login_stat = "owner_login"
    global global_fullname
    if request.method == 'POST':
        username_owner_input = request.form.get("username-owner")
        email_owner_input = request.form.get("email-owner")
        password_owner_input = request.form.get("password-owner")
        username_tenant_input = request.form.get("username-tenant")
        email_tenant_input = request.form.get("email-tenant")
        password_tenant_input = request.form.get("password-tenant")
        login_stat = request.form.get("login_status")

        if login_stat == "owner_login":
            user_record = users_data.find_one({
                'username': username_owner_input,
                'email': email_owner_input,
                'password': password_owner_input,
                'role': 'owner'
            })

            if user_record:
                global_fullname = f"{user_record['firstname']} {user_record['lastname']}"
                return redirect(url_for('home_page'))
            else:
                return render_template('login.html', login_status=login_stat)

        elif login_stat == "tenant_login":
            user_record = users_data.find_one({
                'username': username_tenant_input,
                'email': email_tenant_input,
                'password': password_tenant_input,
                'role': 'tenant'
            })

            if user_record:
                global_fullname = f"{user_record['firstname']} {user_record['lastname']}"
                return redirect(url_for('home_page_tenant'))
            else:
                return render_template('login.html', login_status=login_stat)

    return render_template('login.html', login_status=login_stat)

# This is for signup page for somebody wants to signup as an owner
@app.route('/signup', methods=['POST', 'GET'])
def signup_page():
    if request.method == 'POST':
        if (not validate_password(request.form['password']) or
            not validate_email(request.form['email']) or
            not validate_birthday(request.form['birthday'])):
            return render_template('signup.html')

        if (users_data.find_one({'username': request.form['username'], 'role': 'owner'}) or
            users_data.find_one({'email': request.form['email'], 'role': 'owner'})):
            return render_template('signup.html')

        user = User(request.form['username'], request.form['firstname'], request.form['lastname'],
                    request.form['password'], request.form['email'], request.form['birthday'], Role='owner')

        d = dict(user.__dict__)
        users_data.insert_one(d)
        global_fullname = f"{request.form['firstname']} {request.form['lastname']}"
        return redirect(url_for('home_page', fullname=global_fullname))

    return render_template('signup.html')

# This is for signup page for somebody wants to signup as a tenant
@app.route('/signup2', methods=['POST', 'GET'])
def signup_page2():
    if request.method == 'POST':
        if (not validate_password(request.form['password']) or
            not validate_email(request.form['email']) or
            not validate_birthday(request.form['birthday'])):
            return render_template('signup2.html')

        if (users_data.find_one({'username': request.form['username'], 'role': 'tenant'}) or
            users_data.find_one({'email': request.form['email'], 'role': 'tenant'})):
            return render_template('signup2.html')

        user = User(request.form['username'], request.form['firstname'], request.form['lastname'],
                    request.form['password'], request.form['email'], request.form['birthday'], Role='tenant')

        d = dict(user.__dict__)
        users_data.insert_one(d)
        global_fullname = f"{request.form['firstname']} {request.form['lastname']}"
        return redirect(url_for('home_page_tenant'))

    return render_template('signup2.html')

# ----------------------------------------------------------------------------------------------
# **************     Owner    ***************************************************
# Route for owner home page
@app.route('/home/', methods=['GET', 'POST'])
def home_page():
    property_list = []
    if request.method == 'POST':
        property_list = property_owner_data.find()
    return render_template('home.html', full_name=global_fullname, property_owner_list=property_list)

# Route for owner add home page
@app.route('/home/addhome_owner', methods=['GET', 'POST'])
def home_owner_to_addhome():
    if request.method == 'POST':
        house_name = request.form['property_name']
        location = request.form['location']
        rent_price = request.form['rent_price']
        rent_period = request.form['rent_period']
        description = request.form['description']
        card_number = request.form['owner_card_number']
        fullname = global_fullname

        current_time = datetime.now()
        current_date = current_time.date().isoformat()
        current_time = current_time.time().strftime('%H:%M:%S')

        property_owner_data.insert_one({
            'owner': fullname,
            'property_name': house_name,
            'location': location,
            'rent_price': rent_price,
            'rent_period': rent_period,
            'description': description,
            'owner_card_number': card_number,
            'date': current_date,
            'time': current_time
        })

    return render_template('addhome_owner.html', full_name=global_fullname)

# Route for owner contact page
@app.route('/home/contact', methods=['GET', 'POST'])
def contact_page_owner():
    return render_template('contact.html')

# Route for owner show page
@app.route('/home/show_home_owner', methods=['GET', 'POST'])
def show_page_owner():
    property_list = property_owner_data.find({'owner': global_fullname})
    return render_template('show_home_owner.html', full_name=global_fullname, property_owner_list=property_list)

@app.route('/home/playlist')
def playlist_page():
    return render_template('playlist.html', full_name=global_fullname)

# **********************   Tenant ****************************************
# Route for tenant home page
@app.route('/home2', methods=['GET', 'POST'])
def home_page_tenant():
    property_list = []
    if request.method == 'POST':
        property_list = property_owner_data.find()
    return render_template('hometenant.html', full_name=global_fullname, property_owner_list=property_list)

# Route for tenant rent home page
@app.route('/home2/rent_tenant', methods=['GET', 'POST'])
def add_page_tenant():
    return render_template('rent_tenant.html', full_name=global_fullname)

# Route for tenant contact page
@app.route('/home2/contact', methods=['GET', 'POST'])
def contact_page_tenant():
    return render_template('contact.html')

# Route for tenant show home page
@app.route('/home2/show_page_tenant', methods=['GET', 'POST'])
def show_page_tenant():
    return render_template('show_home_tenant.html', full_name=global_fullname)

@app.route('/<objectID>/home2/playlist')
def playlist_page2(objectID):
    current_property = property_owner_data.find_one({'_id': ObjectId(objectID)})
    return render_template('playlist2.html', full_name=global_fullname, property=current_property)


@app.route('/transfer_funds', methods=['POST'])
def transfer_funds():
    new_balance = None
    from_card_number = request.form.get('from_card_number')  # using get to avoid KeyError
    from_cardholder_name = request.form.get('from_cardholdername')
    to_card_number = request.form.get('to_card_number')

    # Check if all fields were filled in the form
    if not from_card_number or not from_cardholder_name or not to_card_number:
        flash("Please fill in all fields.", "error")
        return render_template('integrated_payment.html', new_balance=new_balance)

    try:
        amount_to_transfer = float(request.form.get('amount', 0))  # using get with a default value
    except ValueError:
        flash("Invalid amount. Please enter a valid number.", "error")
        return render_template('integrated_payment.html', new_balance=new_balance)

        # Find the source card
    from_card_info = cards_data.find_one({
        "card_number": from_card_number,
        "cardholdername": from_cardholder_name
    })

    # Find the destination card
    to_card_info = cards_data.find_one({
        "card_number": to_card_number
    })

    if from_card_info and to_card_info:
        try:
            from_balance = float(from_card_info['balance'])
            to_balance = float(to_card_info['balance'])

            # Check if there are sufficient funds
            if from_balance >= amount_to_transfer:
                # Deduct from the source card
                cards_data.update_one(
                    {"card_number": from_card_number},
                    {"$set": {"balance": from_balance - amount_to_transfer}}
                )
                # Add to the destination card
                cards_data.update_one(
                    {"card_number": to_card_number},
                    {"$set": {"balance": to_balance + amount_to_transfer}}
                )

                new_balance = from_balance - amount_to_transfer
                flash(f"The amount of {amount_to_transfer} has been successfully transferred.", "success")

                # Redirect to playlist2 after a successful transfer
                return redirect(url_for('playlist_page2',
                                        objectID=to_card_info['_id']))  # Assumes you want to redirect to playlist2

            else:
                flash("Insufficient funds in the source account.", "error")
        except ValueError:
            flash("Current balance is not numeric. Please correct this in the database.", "error")
    else:
        flash("Cardholder name or card number is incorrect for one or both accounts.", "error")

    return render_template('integrated_payment.html', new_balance=new_balance)
if __name__ == '__main__':
    app.run(debug=True)