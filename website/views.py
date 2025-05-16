from flask import Blueprint, render_template, flash, redirect, request
from .models import Product, Basket
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__) #initialising blueprint for each page

@views.route('/')
def home():

    items = Product.query.order_by(Product.productName).all()
    return render_template('home.html', items=items)



@views.route('/add-to-basket/<int:itemID>')
@login_required
def addToBasket(itemID):
    itemToAdd = Product.query.get(itemID) #gets the item clicked ID
    itemExists = Basket.query.filter_by(productLink = itemID, customerLink=current_user.id).first()#Checks if the item exists in user's basket
    if itemExists:
        try:
            itemExists.quantity = itemExists.quantity + 1 #if the user already has one in their basket adds one
            db.session.commit() #updates the database
            flash('updated')
            return redirect(request.referrer) #redirects user straight back to the homepage
        except Exception as e:
            print('Item not updated', e) #prints the issue
            flash('not updated')
            return redirect(request.referrer)
    
    newBasketItem = Basket() #if it's new in the basket
    newBasketItem.quantity = 1
    newBasketItem.productLink = itemToAdd.id #adds the item to the basket
    newBasketItem.customerLink = current_user.id
    try:
        db.session.add(newBasketItem) #commits it to the table
        db.session.commit()
        flash('Product has been added')

    except Exception as e:
        print('Error occured', e)
        flash('Did not work')
    return redirect(request.referrer)

@views.route('/basket')
@login_required
def showBasket():
    basket = Basket.query.filter_by(customerLink=current_user.id).all() #filters by the user currently logged in
    amount = 0
    for item in basket:
        amount += item.product.price * item.quantity #multiplies to get the total amount
    return render_template('basket.html', basket=basket, total=amount)

@views.route('/delete/<int:itemID>', methods=['GET', 'POST'])
@login_required
def deleteItem(itemID):

    try:
        itemToDelete=Basket.query.get(itemID) #gets the item ID of the product they want to delete
        db.session.delete(itemToDelete) #deletes it from the database
        db.session.commit() #commits that delete
        flash('Item deleted')
        return redirect('/basket')
    except Exception as e:
        print('ITem not deleted', e)
        flash('Item not deleted')
    return redirect('/basket')

@views.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

@views.route('/pay', methods=['Get', 'POST'])
@login_required
def deleteBasket():
    try:
        db.session.query(Basket).delete() #deletes all of the users items
        db.session.commit()
        flash('Item deleted')
        return redirect('/')
    except Exception as e:
        print('ITem not deleted', e)
        flash('Item not deleted')
    return redirect('/checkout')

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        searchQuery = request.form.get('search')
        items = Product.query.filter(Product.productName.ilike(f'%{searchQuery}%')).all() #checks the database for anything containing the string searched
        return render_template('search.html', items=items)
    return render_template('search.html')