from flask import Blueprint, render_template, request, flash, jsonify
# from .config import config
# from database import fun
import os


import random
import psycopg2
import datetime
import pytz
import string


views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'png'}

@views.route('/', methods=["GET", "POST"])
def index():
    # conn = None
    # data = None
    # try:
    #     params = config()
    #     n = random.randint(1, 3226)
    #     conn = psycopg2.connect(**params)

    #     print('Connected succesfully')
    #     cur = conn.cursor()

    #     data = cur.fetchall()

    # except(Exception, psycopg2.Error) as error:
    #     print(error)

    # finally:
    #     if conn is not None:
    #         cur.close()
    #         conn.close()

    return render_template('index.html')

@views.route("/quadratic_descr", methods=["GET", "POST"])
def quadratic_descr():
    return render_template("quadratic_descr.html")

