#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_login import login_user, logout_user
import database.database as db


auth = Blueprint('auth', __name__)

# TODO: ustawić poprawnie query
@auth.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = db.User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            if login_user(user, remember=True):
                response = make_response(jsonify(result=True, id=user.id))
            else:
                response = make_response(jsonify(result=False, id=None))
        else:
            response = make_response(jsonify(result=False, id=None))
    else:
        response = make_response(jsonify(result=False, id=None))
    response.headers["Content-Type"] = "application/json"
    return response


@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    res = logout_user()
    if res:
        response = make_response(jsonify(result=True))
    else:
        response = make_response(jsonify(result=False))
    response.headers["Content-Type"] = "application/json"
    return response


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user_by_email = db.User.query.filter_by(email=email).first()
    user_by_username = db.User.query.filter_by(username=username).first()
    if user_by_email or user_by_username:
        flash('User already exists.', category='error')
        return redirect(url_for('auth.sign-up'))
    new_user = [{'email': email, 'username': username, 'password': generate_password_hash(password, method='sha256')}]
    db.insert_to_table(db.db_con, db.meta, 'User', new_user)
    return redirect(url_for('auth.login'))


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    return False
