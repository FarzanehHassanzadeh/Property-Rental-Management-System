Certainly! Here's the text translated to English:

```markdown
# Property Rental Management System

## Overview
**Property Rental Management System** is an online real estate system that allows property owners to list their properties for rent and tenants to search and book desired properties. This system uses MongoDB to store property listings, rental agreements, and user profiles. Features of this system include property reviews, booking calendars, and payment integration.

## Prerequisites
- Python
- PyCharm
- MongoDB

## Installation and Setup
1. Clone the repository:
   ```shell
   git clone https://github.com/FarzanehHassanzadeh/Property-Rental-Management-System.git
   cd PropertyRentalManagementSystem
   ```

2. Install dependencies:
   ```shell
   pip install -r requirements.txt
   ```

3. Start MongoDB:
   ```shell
   docker run --name mongo -d -p 27017:27017 -v "$PWD/db:/data/db" mongo:latest
   ```

4. Run the project:
   - Open the project in PyCharm and run it.

## Usage
1. After running the program, open `http://127.0.0.1:5000` in your browser and go to the `start` page.
2. There are several buttons at the top of the page:
   - **About**: Information about the site owners and the site itself.
   - **Contact Us**: Contact the site owners via email, etc.
3. To log in to the site, select the **Log In** button at the top of the page.
4. On the **Log In** page:
   - If you have an account, log in using your `username`, `password`, and `email`.
   - Choose your role as either **Owner** or **Tenant**.
5. If you are not registered, click the **Sign Up** button and fill out the registration form. Make sure to specify whether you are registering as an Owner or Tenant.
6. After successful registration and login, owners and tenants are directed to their respective sections.

### Owners:
   - Click on **Add** to list your properties for sale or rent.
   - On the **Home Owner** page, use the magnifying glass at the top of the page to view properties you have listed for rent or sale.
   - After viewing the properties, you can delete any property listed for rent or sale.
   - Use **View Profile** to access your profile and view information such as name, country, birth date, and the calendar of rented properties.

### Tenants:
   - After logging into their **Home** page, tenants can use the magnifying glass at the top of the page and property features to search for desired properties. 
   - Use the **Show Details** button to view property details and then click on **Payment** to proceed to the payment page.
   - On the payment page, tenants can enter their card information to make a payment and become the owner of the property. Note that the payment page has a timer and will redirect to the tenant's **Home** page after 120 seconds.
   - The **Home** page for tenants includes a field for easier property search using criteria such as rent period, owner name, rent price, and location.
   - On the **Show** page, tenants can view properties they have rented and pay the rent, whether monthly or weekly.
   - Use **View Profile** to access and view profile information such as name, country, birth date, and the calendar of rented properties.

## Features
- **User Registration and Login**: Users can register and log in as owners or tenants.
- **List Properties**: Owners can list their properties for rent.
- **Search and Book Properties**: Tenants can search and book properties.
- **Property Reviews**: Users can review and rate properties.
- **Booking Calendar**: Calendar display for property booking.
- **Payment Integration**: Online rent payment capability.

## Contact
For questions, suggestions, and issues, please contact:
- **Email**: hsnzadhfrzanh234@gmail.com
- **Email**: kiarsh.dalir2003@gmail.com
```

Feel free to make any adjustments or let me know if there are additional details you'd like to include!
