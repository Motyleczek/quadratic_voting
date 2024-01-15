from flask import Blueprint, render_template, request, flash, jsonify
# from .config import config
# from database import fun
from flask_login import login_required
import os


import random
import psycopg2
import datetime
import pytz
import string

import database.database_definitions
import database.db_functions
import voting.voting

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
@login_required
def vote_creation():
    title : str = None
    data_start : datetime = None
    data_end : datetime = None
    vote_type : str = None # TODO: mozna by to przerobic na enuma
    num_credits : int = None
    vote_options: List[str] = []
    
    # data to create the correct user list
    vote_users = database.db_functions.get_voters_createdby_user(session, current_user.username)
    data= []
    for elem in vote_users:
        data.append({'name': elem})
    
    
    if request.method == "POST":
       # getting input with name = fname in HTML form
       title = request.form.get("title")
       # getting input with name = lname in HTML form 
       data_start = request.form.get("data_start")
       data_end = request.form.get("data_end")
       vote_type = request.form.get("vote_type")
       num_credits = request.form.get("credits")
       
       # all fields starting with input --> will be the vote options
       print(request.form.getlist('selected_options[]'))
       for key in request.form.keys():
           print(key)
           if len(key) >= 6:
            if key[:5] == 'input':
                    vote_option_x = request.form.get(key)
                    vote_options.append(vote_option_x)
        
       # TODO odkomentować po testach
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
       
       chosen_users = request.form.getlist('selected_options[]')
       database.db_functions.add_users_to_voting(session, vote_id, chosen_users, current_user.username)
    
        
    
    return render_template("vote_creation.html", data = data)

@views.route("/voting", methods=["GET", "POST"])
@login_required
def choose_vote():
     
    # testing = database.db_functions.get_voter_votings(session, current_user.id)
    # print(testing)
    
    vote_deets = database.db_functions.get_voter_votings(session, current_user.id)
    
    votes_options_dict = {}
    votes_credit_dict = {}
    
    vote_name_to_id = {}
    option_name_to_id = {}
    
    for vote in vote_deets:
        vote_id, vote_name = vote
        vote_name_to_id[vote_name] = vote_id
        
        option_list, credit = database.db_functions.get_voting_parameters(session, vote_id)
        vote_options =[]
        for option in option_list:
            option_id, option_name = option
            option_name_to_id[option_name] = option_id
            vote_options.append(option_name)
        
        votes_credit_dict[vote_name] = credit
        votes_options_dict[vote_name] = vote_options
        
    
    test_data = [{'votes_opt_dicts': votes_options_dict},
                  {'votes_credit_dict': votes_credit_dict}]
    
    
    if request.method == 'POST':
        print(request.form.keys())
        result_dict = {}
        vote_id = None
        for key, val in request.form.items():
            if key == "vote_name":
                vote_id = vote_name_to_id[val]
                continue
            vote_opt = key
            vote_credit_val = val
            vote_opt_id = option_name_to_id[vote_opt]
            result_dict[vote_opt_id] = int(vote_credit_val)

        voting.voting.vote(session, current_user.id, vote_id, current_user.username, result_dict, votes_credit_dict[vote_name])
    
    return render_template("choose_vote.html", data=test_data)