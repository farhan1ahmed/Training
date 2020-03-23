from flask import Blueprint, render_template, flash, redirect, url_for, request
from .forms import UserRegistrationForm, UserLoginForm
from app import bcrypt, db
from app.database_structure import UserModel
from flask_login import login_user as LogUserIn, current_user, logout_user


mod_register_login = Blueprint('register', __name__)
@mod_register_login.route("/register", methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('webapp.hello'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserModel(Username=form.username.data, Email=form.email.data, Password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! \n Please Login', 'success')
        return redirect(url_for('register.login_user'))
    return render_template('register.html', title='Register', form=form)


@mod_register_login.route("/login", methods=['GET', 'POST'])
def login_user():
    if current_user.is_authenticated:
        return redirect(url_for('webapp.hello'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            LogUserIn(user, remember=form.remember.data)
            nextpage = request.args.get('next')
            return redirect(nextpage) if nextpage else redirect(url_for('webapp.hello'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@mod_register_login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('register.login_user'))

