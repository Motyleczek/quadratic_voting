#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_login import login_user, logout_user, LoginManager, current_user
from website import Website
import database.database_definitions as db
import database.db_functions as dbf
import pandas as pd

auth = Blueprint('auth', __name__)
website = Website()
session = db.Session()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(website.app)


@login_manager.user_loader
def load_user(user_id):
    user = session.query(db.User).filter(db.User.id == user_id and db.User.active == 1).first()
    return user


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = dbf.get_user_login(session, username=username)
        if user:
            if check_password_hash(user.password, password):
                if login_user(user, remember=remember):
                    flash("Logged in successfully!", category='success')
                    user.is_authenticated = True
                    # print(dbf.get_user_login(session, username=username))
                    # print(dbf.get_user_role(session, current_user.username))
                    return redirect(url_for("views.index"))
            else:
                flash("Incorrect password!", category='error')
        else:
            flash("User does not exist!", category='error')
    return render_template('login.html')


@auth.route('/logout')
def logout():
    current_user.is_authenticated = False
    logout_user()
    return redirect(url_for("views.index"))

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        print(role, type(role))
        user_by_email = session.query(db.User).filter(db.User.email == email and db.User.is_active == 1).first()
        user_by_username = dbf.get_user_login(session, username=username)
        print(user_by_email, user_by_username)
        if user_by_email or user_by_username:
            flash('User already exists.', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif len(password) < 5:
            flash('Password must be at least 5 characters.', category='error')
        else:
            dbf.insert_new_user(session, username, generate_password_hash(password), email, role)
            flash('Account created successfully', category='success')
    return render_template("sign_up.html")


@auth.route('/add_users', methods=['POST', 'GET'])
def add_users():
    if request.method == 'POST':
        uploaded_file = request.files['fileInput']
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if uploaded_file:
            print("Tutaj będzie dodawanie z pliku")
            if uploaded_file and uploaded_file.filename.endswith('.csv'):
                csv_data = pd.read_csv(uploaded_file)
                # for i in range(len())
                # print(len(csv_data))
            # tutaj dodać obsługę pliku dodawania użytkowników z listy
        else:
            add_voter(username, email, password)
    return render_template("add_users.html")

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def add_voter(username, email, password):
    user_by_email = session.query(db.User).filter(db.User.email == email and db.User.is_active == 1).first()
    user_by_username = dbf.get_user_login(session, username=username)
    print(user_by_email, user_by_username)
    if user_by_email or user_by_username:
        flash('User already exists.', category='error')
        return redirect(url_for('auth.add_users'))
    elif len(username) < 2:
        flash('Username must be greater than 1 character.', category='error')
    elif len(password) < 5:
        flash('Password must be at least 5 characters.', category='error')
    else:
        dbf.insert_new_user(session, username, generate_password_hash(password), email, "Voter", current_user.username)
        flash('Account created successfully', category='success')