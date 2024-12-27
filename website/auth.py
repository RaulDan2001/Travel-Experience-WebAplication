from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #cer datele de la utilizator
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        #verific daca emailul si parola introduse sunt corecte
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in succesfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.mytrips'))
            else:
                flash("Wrong password, try again!", category='error')
        else:
            flash("There is no user with this email, create a new account!", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already in use', category='error')
        elif len(email) < 4:
            flash("You must enter a valid email address!!", category="error")
        elif len(firstName) < 2:
            flash("You must enter a valid Name!!", category='error')
        elif len(lastName) < 2:
            flash("You must enter a valid Name!!", category='error')
        elif len(password1) < 8: 
            flash("Password must be at least 8 characters!!", category='error')
        elif password1 != password2:
            flash("The passwords do not match!!", category='error')
        else:
            #adaug un utilizator nou
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully!!", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.mytrips'))

    return render_template("sign_up.html", user=current_user)