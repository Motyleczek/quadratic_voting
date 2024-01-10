from flask import Blueprint, render_template, request, flash, jsonify
# from .config import config
# from database import fun
import os


import random
import psycopg2
import datetime
import pytz
import string

import database

from typing import List

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'png'}

@views.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@views.route("/quadratic_descr", methods=["GET", "POST"])
def quadratic_descr():
    return render_template("quadratic_descr.html")


@views.route("/vote_creation", methods=["GET", "POST"])
def vote_creation():
    title : str = None
    data_start : datetime = None
    data_end : datetime = None
    vote_type : str = None # TODO: mozna by to przerobic na enuma
    num_credits : int = None
    vote_options: List[str] = []
    
    if request.method == "POST":
       # getting input with name = fname in HTML form
       title = request.form.get("title")
       # getting input with name = lname in HTML form 
       data_start = request.form.get("data_start")
       data_end = request.form.get("data_end")
       vote_type = request.form.get("vote_type")
       num_credits = request.form.get("credits")
       for key in request.form.keys():
           if len(key) >= 6:
            if key[:5] == 'input':
                    vote_option_x = request.form.get(key)
                    vote_options.append(vote_option_x)
       
       
    
    return render_template("vote_creation.html")