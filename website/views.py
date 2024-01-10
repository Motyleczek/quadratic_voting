from flask import Blueprint, render_template, request, flash, jsonify
# from .config import config
# from database import fun
import os


import random
import psycopg2
import datetime
import pytz
import string

import database.database_definitions
import database.db_functions

from typing import List
from flask_login import current_user

views = Blueprint('views', __name__)

session = database.database_definitions.Session()

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
       
       vote_id = database.db_functions.create_voting(session, 
                              name=title,
                              start_date = data_start,
                              end_date = data_end,
                              author = current_user.username,
                              credits = num_credits,
                              type_ = vote_type)
       database.db_functions.add_options_to_voting(session,
                                      voteid=vote_id,
                                      option_list=vote_options,
                                      createdby=current_user.username)
        
    
    return render_template("vote_creation.html")

@views.route("/voting", methods=["GET", "POST"])
def choose_vote():
    return render_template("choose_vote.html")