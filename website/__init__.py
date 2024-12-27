from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    #initializez aplicatia
    app = Flask(__name__)
    #configurez o cheie secreta pentru criptare
    app.config['SECRET_KEY'] = 'EK5qVn2kUwzZQN4T7rAFug'
    #conectez flask la baza de date
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #importez blueprint-uri
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #importez acest fisier pentru a ma asigura ca se creeaza modelele pentru baza de date
    from .models import User, Trip

    create_database(app)

    #menajez login-urile de pe site si logout-urile
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        print(f"Loading user with id: {id}")
        return User.query.get(int(id))
    
    @app.context_processor
    def inject_user():
        print(f"Injecting user: {current_user}")
        return dict(user=current_user)
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database!!")