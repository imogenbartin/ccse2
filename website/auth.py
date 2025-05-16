from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, RegisterForm, PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) #initialising blueprint for each page needing authorisation


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): #checks it is a post request and valid - inbuilt flask function
        email = form.email.data #takes form data and assigns it to a variable
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first() #sqlalchemy filter, just grabs the first instance to save time as there should only be one
        
        if customer:
            if customer.verifyPassword(password=password):
                login_user(customer) #built in flask command with sessions
                if current_user.id == 1:
                    return redirect('/shop-items')
                else:
                    
                    return redirect('/')
            else:
                print("Incorrect Password")        
        else:
            print('Account doesn not exist')

    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data #takes form data and assigns it to a variable
        username = form.username.data
        password = form.password.data
        confirmPassword = form.confirmPassword.data

        if password == confirmPassword: #checks password and confirm password fields are the same
            newCustomer = Customer() #calling the class in models.py 
            newCustomer.email = email #assigning the email to the email field in the database, etc
            newCustomer.username = username
            newCustomer.password = password #don't need to hash because there's a function in the Customer class of models.py that does it

            try:
                db.session.add(newCustomer) #adds the new session to the database
                db.session.commit()
                flash('Account created successfully') #shows the user the message
                return redirect('/login') #redirects the user to the login page

            except Exception as e: #if it didn't work
                print(e)
                flash('Account creation failed, email already exists') #a user has already used the email so tells the user
            
            form.email.data = '' #resets all the values back to nothing
            form.username.data = ''
            form.password.data = ''
            form.confirmPassword.data = ''

    return render_template('register.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logOut():
    logout_user()
    return redirect('/login')

@auth.route('/account/<int:customerID>') #makes the link change depending on the customer
@login_required #makes it so the user must be logged in to view
def account(customerID):
    customer = Customer.query.get(customerID)
    
    return render_template('account.html')

@auth.route('/change-password/<int:customerID>', methods=['GET', 'POST'])
@login_required
def changePassword(customerID):
    form = PasswordChangeForm() #gets the form from forms.py

    customer = Customer.query.get(customerID) #getting customer ID from the Customer database
    if form.validate_on_submit(): #if all inputs are valid
        currentPassword = form.currentPassword.data #getting data from the form
        newPassword = form.newPassword.data
        confirmNewPass = form.confirmNewPass.data

        if customer.verify_password(currentPassword): #verifying the current password is the same as in the table
            if newPassword == confirmNewPass: #confirming the new password is the same as confirm password
                customer.password = confirmNewPass #making the password the new one
                db.session.commit() #committing it to the table
                flash('password updated successfully') #telling the user it's right
                return redirect(f'/profile/{customer.id}') #redirecting back to the account page
        else:
            flash('current pass is incorrect')

    return render_template('changePassword.html', form=form)

