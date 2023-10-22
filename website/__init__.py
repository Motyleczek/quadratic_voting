#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
# from ..database import *

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# def createMemeTable(db):

#     class MemeTable(db.Model):

#         __tablename__ = 'MemeTable'
#         key = db.Column(db.Integer, primary_key=True, autoincrement=True)
#         title = db.Column(db.String)
#         thumbnail = db.Column(db.String)
#         height = db.Column(db.Integer)
#         width = db.Column(db.Integer)
#         time = db.Column(db.Integer)
#         author = db.Column(db.String)
#         id = db.Column(db.String)
#         ups = db.Column(db.Integer)
#         downs = db.Column(db.Integer)
#         media = db.Column(db.String)
#         sentiment = db.Column(db.String)
#         humour = db.Column(db.String)
#         sarcasm = db.Column(db.String)
#         offensive = db.Column(db.String)
#         motivational = db.Column(db.String)

#     return MemeTable

# here we are ensuring that the values in .env are imported into Website, nice
class Website(metaclass=SingletonMeta):
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ["APP_SECRET"]
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'

        self.db = SQLAlchemy(self.app)

        # register all models here
        # self.MemeTable = createMemeTable(self.db)

        # with self.app.app_context():
        #     self.db.create_all()
            
        #     if self.MemeTable.query.count() == 0:
        #         self.set_initial_values()
        #         print('Database schema has been synchronized')
        #     else:
        #         print('MemeTable already exists in the database, skipping initialization.')

    # def set_initial_values(self):
    #     with open("meme_recommender/dataset/db.csv", encoding='utf8') as file:
    #         data = csv.reader(file)
    #         next(data)

    #         for row in data:
    #             key, title, thumbnail, height, width, time, author, meme_id, ups, downs, media, sentiment, humour, sarcasm, offensive, motivational = row
    #             new_meme = self.MemeTable(
    #                 # key=key,
    #                 title=title,
    #                 thumbnail=thumbnail,
    #                 height=height,
    #                 width=width,
    #                 time=time,
    #                 author=author,
    #                 id=meme_id,
    #                 ups=ups,
    #                 downs=downs,
    #                 media=media,
    #                 sentiment = sentiment,
    #                 humour = humour,
    #                 sarcasm = sarcasm,
    #                 offensive = offensive,
    #                 motivational = motivational 
    #             )
    #             self.db.session.add(new_meme)
    #         self.db.session.commit()