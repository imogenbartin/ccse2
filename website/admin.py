from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from .forms import ShopItemsForm
from werkzeug.utils import secure_filename
from .models import Product
from . import db


admin = Blueprint('admin', __name__) #initialising blueprint for each admin page

@admin.route('/media/<path:filename>')
def getImage(filename):
    return send_from_directory('../media', filename)

@admin.route('/add-shop-items', methods=['POST', 'GET'])
@login_required
def addShopItems():
    print(current_user.id)
    if current_user.id == 1: #makes sure only people with admin can log in 
        form = ShopItemsForm() #gets the form from form.py
        if form.validate_on_submit(): 
            productName = form.productName.data
            price = form.price.data
            itemAmount = form.itemAmount.data
            productPicture = form.productPicture.data

            productFile = secure_filename(productPicture.filename) #returns a santised version of the filename
            productFilePath = f'./media/{productFile}' #shows where the images are kept

            productPicture.save(productFilePath) #saves the product picture to the media folder

            newShopItem = Product() #saving all the data to the product table
            newShopItem.productName = productName
            newShopItem.price = price
            newShopItem.itemAmount = itemAmount
            newShopItem.productPicture = productFilePath

            try: #adding to database
                db.session.add(newShopItem) 
                db.session.commit()
                flash (f'{productName} added successfully') #tells the admin it's been added successfully
                print('Item added')
                return render_template('add-shop-items.html', form=form)
            except Exception as e:
                print(e) #prints exception to the console
                flash('Item has not been added')

        return render_template('add-shop-items.html', form=form)
    
    return render_template('404.html')

@admin.route('/shop-items', methods=['GET','POSTS'])
@login_required
def shopItems():
    if current_user.id == 1: #if current user is an admin
        items = Product.query.order_by(Product.dateAdded).all() #sort the table of products by date added
        return render_template('shop-items.html', items=items)
        
    return render_template('404.html')


@admin.route('/update-item/<int:itemID>', methods=['GET', 'POST'])
@login_required
def updateItem(itemID):
    if current_user.id == 1:
        form = ShopItemsForm()

        itemToUpdate = Product.query.get(itemID)

        form.productName.render_kw = {'placeholder': itemToUpdate.productName} #writing in the placeholders as the previous ones
        form.price.render_kw = {'placeholder': itemToUpdate.price}
        form.itemAmount.render_kw = {'placeholder': itemToUpdate.itemAmount}

        if form.validate_on_submit(): #form data like in adding products
            productName = form.productName.data
            price = form.price.data
            itemAmount = form.itemAmount.data
            productPicture = form.productPicture.data

            productFile = secure_filename(productPicture.filename) #returns a santised version of the filename
            productFilePath = f'./media/{productFile}' #shows where the images are kept

            productPicture.save(productFilePath)

            try:
                Product.query.filter_by(id=itemID).update(dict(productName=productName,price=price,itemAmount=itemAmount,productPicture=productFilePath))
                db.session.commit() #updating the table in the database
                flash(f'{productName} updated successfully')
                print('Product updated')
                return redirect('/shop-items')
            except Exception as e:
                print('Product not updated', e)


        return render_template('update-item.html', form=form)

    return render_template('404.html')

@admin.route('/delete-item/<int:itemID>', methods=['GET', 'POST'])
@login_required
def deleteItem(itemID):
    if current_user.id == 1:
        try:
            itemToDelete=Product.query.get(itemID) #gets the item ID of the product they want to delete
            db.session.delete(itemToDelete) #deletes it from the database
            db.session.commit() #commits that delete
            flash('Item deleted')
            return redirect('/shop-items')
        except Exception as e:
            print('ITem not deleted', e)
            flash('Item not deleted')
        return redirect('/shop-items')
    return render_template('404.html')