from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DBNAME = 'database.sqlite3'

def createDatabase():
    db.create_all()
    print('Database created')

def createApp(): #function to initialise the application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'INSERTHEREATSOMEPOINT'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DBNAME}'

    db.init_app(app)

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template('404.html')

    loginManager = LoginManager() #keeps track of everyone that logs in and their access tokens
    loginManager.init_app(app) #initialising the login manager
    loginManager.login_view = "auth.login" #tells the login manager where the login view is located in the files

    @loginManager.user_loader #loads the user based on their id
    def loadUser(id):
        return Customer.query.get(int(id)) #retrieves the user for the session


    from .views import views  #imports needed to register blueprints
    from .auth import auth
    from .admin import admin
    from .models import Customer, Basket, Product, Order

    app.register_blueprint(views, url_prefix='/')  #registering the blueprints for the three types of pages
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

  #  with app.app_context():
   #     createDatabase()

    return app