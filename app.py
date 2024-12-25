from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from user import User
import re
from datetime import datetime
from bson.objectid import ObjectId
import secrets  # Import secrets module for generating a secure secret key

global_fullname = ''
a=''
global_email=''
global_objectID_property_owner = ''
global_objectID_property_tenant = ''
time_property=''
global_birthday=''
global_username=''
global_img=''

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
property_tenant_data = db['property_tenant_data']
cards_data = db['Cards_data']
contacts_data = db['Contacts_data']

# This function is used for the start page
@app.route('/', methods=['GET', 'POST'])
def start_page():
    return render_template('start.html')

# ******************************************************
# This Function is used for login page
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login_stat = "owner_login"
    global global_fullname,global_email,global_birthday,global_username,global_img
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
                global_email=user_record['email']
                global_birthday = user_record['birthday']
                global_username= user_record['username']
                global_img= user_record['img']

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
                global_birthday = user_record['birthday']
                global_email = user_record['email']
                global_username = user_record['username']
                global_img = user_record['img']
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
@app.route('/signup3', methods=['POST', 'GET'])
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
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    # property_list = []
    # if request.method == 'POST':
    #     search_property_name = request.form['search_box']
    #     if search_property_name == '':
    #          property_list = property_owner_data.find()
    #     else:
    #
    #          property_list = property_owner_data.find({'property_name':{'$regex': search_property_name,
    #                                                                     '$options': 'i'}}) # '$options': 'i' is for no being case-sensitive

    property_list = []

    search_property_name = ''
    date_property = ''
    time_property = ''
    amount_property = ''

    if request.method == 'POST':
        search_property_name = request.form['search_box']

        owner_property = request.form.get('owner')
        location_property = request.form.get('location')
        rent_price_property = request.form.get('rent_price')
        rent_period_property = request.form.get('rent_period')
        myQuery = {}

        if owner_property and owner_property != '':
            myQuery['owner'] = {'$regex': str(owner_property), '$options': 'i'}
        if location_property and location_property != '':
            myQuery['location'] = {'$regex': str(location_property), '$options': 'i'}
        if rent_price_property and rent_price_property != '':
            myQuery['rent_price'] = '$' + str(rent_price_property)
        if rent_period_property and rent_period_property != '':
            myQuery['rent_period'] = str(rent_period_property)
        if search_property_name and search_property_name != '':
            myQuery['property_name'] = {'$regex': str(search_property_name), '$options': 'i'}
        myQuery['tenant'] = 'Nobody'

        property_list = property_owner_data.find(myQuery)

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
            'time': current_time,
            'rent_status' : 'Nothing'
        })

    return render_template('addhome_owner.html', full_name=global_fullname)

# Route for owner contact page
@app.route('/home/contact', methods=['GET', 'POST'])
def contact_page_owner():
    if request.method == 'POST':


        contact_email = request.form['contact_email']
        contact_name = request.form['name']
        contact_msg = request.form['msg']


        contacts_data.insert_one({'email': contact_email, 'name': contact_name, 'msg': contact_msg})


    return render_template('contact.html')

# Route for owner show page
@app.route('/home/show_home_owner', methods=['GET', 'POST'])
def show_page_owner():
    search_property_name = ''

    if request.method == 'POST':
       search_property_name = request.form['search_box']
    if search_property_name == '':
         property_list = property_owner_data.find({'owner': global_fullname})
    else:
         property_list = property_owner_data.find({'property_name': {'$regex': search_property_name,
                                                                    '$options': 'i'}, 'owner': global_fullname})  # '$options': 'i' is for no being case-sensitive
    return render_template('show_home_owner.html', full_name=global_fullname, property_owner_list=property_list)

@app.route('/<objectID>/home/playlist')
def playlist_page(objectID):
    current_property = property_owner_data.find_one({'_id': ObjectId(objectID)})

    return render_template('playlist.html', full_name=global_fullname,property=current_property)


@app.route('/<objectID>/home/playlist/delete', methods=['GET', 'POST'])
def delete_playlist_page(objectID):
    current_property = property_owner_data.find_one({'_id': ObjectId(objectID)})

    # Check if the property exists
    if not current_property:
        flash("Property not found.", "error")
        return redirect(url_for('home_page'))  # Redirect to a relevant page

    # Check the tenant field in the property
    if current_property.get('tenant') == 'Nobody':
        # If tenant is 'Nobody', delete the property
        property_owner_data.delete_one({'_id': ObjectId(objectID)})
        flash("Property deleted successfully.", "success")
        return "<h1> The property deleted successfully</h1>"  # Redirect after deletion
    else:
        # If the property is rented, show an appropriate message
        flash("This property is currently rented and cannot be deleted.", "error")
        return "<h1>The property is currently rented and cannot be deleted.</h1>"

# Make sure to define routes for 'some_other_page' or handle redirection appropriately
# **********************   Tenant ****************************************
# Route for tenant home page
@app.route('/home2', methods=['GET', 'POST'])
def home_page_tenant():
    property_list = []

    search_property_name =''
    date_property = ''
    time_property = ''
    amount_property = ''


    if request.method == 'POST':
        search_property_name = request.form['search_box']

        owner_property = request.form.get('owner')
        location_property = request.form.get('location')
        rent_price_property =request.form.get('rent_price')
        rent_period_property = request.form.get('rent_period')
        myQuery = {}

        if  owner_property and owner_property != '' :
            myQuery['owner'] = {'$regex': str(owner_property), '$options': 'i'}
        if location_property and location_property != '':
            myQuery['location'] = {'$regex': str(location_property), '$options': 'i'}
        if rent_price_property and rent_price_property != '':
            myQuery['rent_price'] = '$' + str(rent_price_property)
        if rent_period_property and rent_period_property != '':
            myQuery['rent_period'] = str(rent_period_property)
        if search_property_name and search_property_name != '':
            myQuery['property_name'] = {'$regex': str(search_property_name), '$options': 'i'}
        myQuery['tenant'] = 'Nobody'

        property_list = property_owner_data.find(myQuery)
    return render_template('hometenant.html', full_name=global_fullname, property_owner_list=property_list,img=global_img)

# Route for tenant rent home page
@app.route('/home2/rent_tenant', methods=['GET', 'POST'])
def rent_page_tenant():

    return render_template('rent_tenant.html', full_name=global_fullname)

# Route for tenant contact page
@app.route('/home2/contact', methods=['GET', 'POST'])
def contact_page_tenant():

    if request.method == 'POST':
        contact_email = request.form['email']

        contact_name = request.form['name']
        contact_msg = request.form['msg']

        contacts_data.insert_one({'email': contact_email, 'name': contact_name, 'msg': contact_msg})

    return render_template('contact.html')

# Route for tenant show home page
@app.route('/home2/show_page_tenant', methods=['GET', 'POST'])
def show_page_tenant():

    property_list = []

    if request.method == 'POST':

        search_property_name = request.form['search_box']

        owner_property = request.form.get('owner')
        location_property = request.form.get('location')
        rent_price_property = request.form.get('rent_price')
        rent_period_property = request.form.get('rent_period')

        myQuery = {'tenant': global_fullname}

        if owner_property and owner_property != '':
            myQuery['owner'] = {'$regex': str(owner_property), '$options': 'i'}
        if location_property and location_property != '':
            myQuery['location'] = {'$regex': str(location_property), '$options': 'i'}
        if rent_price_property and rent_price_property != '':
            myQuery['rent_price'] = '$' + str(rent_price_property)
        if rent_period_property and rent_period_property != '':
            myQuery['rent_period'] = str(rent_period_property)
        if search_property_name and search_property_name != '':
            myQuery['property_name'] = {'$regex': str(search_property_name), '$options': 'i'}


        property_list = property_owner_data.find(myQuery)

    return render_template('show_home_tenant.html', full_name=global_fullname, property_owner_list=property_list,img=global_img)
@app.route('/<objectID>/home2/show_page_tenant/end_rent', methods=['GET', 'POST'])
def end_renting(objectID):
    global global_objectID_property_owner

    global_objectID_property_owner = objectID
    result = property_owner_data.update_one({'_id': ObjectId(global_objectID_property_owner)}, {'$set': {'tenant': 'Nobody'}})

    if result.modified_count > 0:
        return "<h1>Property renting has been ended successfully.</h1>"
    else:
        return "<h1>there is something wrong</h1>"

@app.route('/<objectID>/home2/show_page_tenant/playlist2', methods=['GET', 'POST'])
def playlist_page2(objectID):
    global global_objectID_property_owner

    global_objectID_property_owner = objectID
    current_property = property_owner_data.find_one({'_id': ObjectId(objectID)})
    return render_template('playlist2.html', full_name=global_fullname, property=current_property,img=global_img)
# -----------------------------------------------------------
# /---------------------------------------------------
# --------------------------------------

app.secret_key = 'your_secret_key'
@app.route('/<objectID>/transfer_funds2', methods=['POST'])
def Payment_on_time(objectID):

    global global_objectID_property_owner, global_fullname, time_property
    current_property = property_owner_data.find_one({'_id': ObjectId(objectID)})
    # objectID = request.form.get('objectID')
    # current_property = property_owner_data.find_one({'_id': ObjectId(objectID)})
    time_property = current_property['date']
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_year, current_month, current_day = current_date.split('-')
    time_year, time_month, time_day = time_property.split('-')

    new_balance = None
    current_month = int(current_month)
    time_month = int(time_month)
    # current_date و time_property
    if current_month == (time_month+1):
        return redirect(url_for('transfer_funds'),objectID)

    else:
        return render_template('start.html')



@app.route('/transfer_funds', methods=['POST'])
def transfer_funds():
    global global_objectID_property_owner, global_fullname
    new_balance = None

    current_property = property_owner_data.find_one({'_id': ObjectId(global_objectID_property_owner)})
    owner_name = current_property['owner']
    firstname, lastname = global_fullname.split()
    owner_firstname, owner_lastname = owner_name.split()
    to_card_data = cards_data.find_one({'cardholdername': owner_firstname})
    # using get to avoid KeyError
    from_card_number = request.form.get('from_card_number')
    from_cardholder_name = firstname
    to_card_number = to_card_data['card_number']

    # Check if all fields were filled in the form
    if not from_card_number or not from_cardholder_name or not to_card_number:
        flash("Please fill in all fields.", "error")
        return render_template('integrated_payment.html', new_balance=new_balance)

    try:
        # amount_to_transfer = float(request.form.get('amount', 0)) # using get with a default value
        amount_to_transfer = float((current_property['rent_price']).replace('$', ''))
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
                property_name = current_property['property_name']
                property_rent_price = current_property['rent_price']
                property_rent_period = current_property['rent_period']
                current_time = datetime.now()
                current_date = current_time.date().isoformat()
                current_time = current_time.time().strftime('%H:%M:%S')
                property_tenant_data.insert_one({'tenant': global_fullname,
                                                 'property_name': property_name,
                                                 'rent_price': property_rent_price,
                                                 'rent_period': property_rent_period,
                                                 'date': current_date,
                                                 'time': current_time})
                property_owner_data.update_one({'_id': ObjectId(global_objectID_property_owner)},
                                               {'$set': {'tenant': global_fullname,
                                                         'date': current_date,
                                                         'time': current_time}})
                flash(f"The amount of {amount_to_transfer} has been successfully transferred.", "success")

                     # Redirect to playlist2 after a successful transfer
                flash(f"The amount of {amount_to_transfer} has been successfully transferred.", "success")

        # Redirect to playlist2 after a successful transfer
                return redirect(url_for('home_page_tenant'))
                # Assumes you want to redirect to playlist2

            else:
               flash("Insufficient funds in the source account.", "error")
        except ValueError:
                       flash("Current balance is not numeric. Please correct this in the database.", "error")

    else:
       flash("Cardholder name or card number is incorrect for one or both accounts.", "error")

    return render_template('integrated_payment.html', new_balance=new_balance)

# Route for tenant rent home page
@app.route('/home2/profile', methods=['GET', 'POST'])
def profile_tenant():

    return render_template('profile.html', full_name=global_fullname,email=global_email,birth=global_birthday,username=global_username,img=global_img)

# Route for tenant rent home page
@app.route('/home/profile', methods=['GET', 'POST'])
def profile_owner():

    return render_template('profileowner.html', full_name=global_fullname,email=global_email,birth=global_birthday,username=global_username,img=global_img)

if __name__ == '__main__':
    app.run(debug=True)