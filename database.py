from email.policy import default
from enum import unique
from django.shortcuts import render
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "xxxxxxxx"

db = SQLAlchemy(app)

# configuring our database uri
# note an error here
username = 'root'
password = 'Mukulrawat2!'
server = "127.0.0.1:3306"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(os.getcwd(), 'movies.db')
app.config['SECRET_KEY'] = "random string"


# basic model
#user registration
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username  = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    reservations = db.relationship('Reservation', backref = 'user', lazy = True)

tags_seat_reservation= db.Table('tags_seat_reservation', 
                            db.Column('seat_id', db.Integer, db.ForeignKey('seat.id'), primary_key = True),
                            db.Column('reservation_id', db.Integer, db.ForeignKey('Reservation.id'), primary_key = True))


class seat(db.Model):
    __tablename__ = 'seat'
    id = db.Column(db.Integer, primary_key=True)
    RowNumber = db.Column(db.Integer)
    screenid = db.Column(db.Integer, db.ForeignKey('screen.id'))
    tags_seat_reservation = db.relationship('Reservation', secondary=tags_seat_reservation, lazy='subquery', backref=db.backref('seats', lazy=True))

class Reservation(db.Model):
    __tablename__ = 'Reservation'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    screenid = db.Column(db.Integer, db.ForeignKey('screen.id'))
    contact = db.Column(db.String(15))
    Reserved = db.Column(db.Boolean, default=False, nullable=False)
    paid = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)


class screen(db.Model):
    __tablename__ = 'screen'
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(64), index=True)
    noOfseats = db.Column(db.Integer)
    shows = db.relationship('show', backref='screen', lazy=True)
    seats = db.relationship('seat', backref='screen', lazy=True)


class genre(db.Model):
    __tablename_ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

class actor(db.Model):
    __tablename_ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

#admin to movies - many to many

tags_admin_movie = db.Table('admin_movie', 
                            db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key = True),
                            db.Column('admin_id', db.Integer, db.ForeignKey('admin.id'), primary_key = True))
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),index=True, unique=True)
    password = db.Column(db.String(64),index=True)
    admin_movie = db.relationship('Movie', secondary=tags_admin_movie, lazy='subquery', backref=db.backref('admins', lazy=True))


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String(64), index=True)
    actor1 = db.Column(db.String(64),index=True)
    actor2 = db.Column(db.String(64),index=True)
    actor3 = db.Column(db.String(64),index=True)
    director = db.Column(db.String(64),index=True)
    language  = db.Column(db.String(64), index=True)
    country  = db.Column(db.String(64), index=True)
    genre = db.Column(db.String(64),index=True)
    description = db.Column(db.String(1000), index=True, nullable=True)
    TimeDuraton = db.Column(db.String(10))
    shows = db.relationship('show', backref='movie', lazy=True)


class show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    showstart  = db.Column(db.DateTime)
    showend = db.Column(db.DateTime)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screen.id'), nullable=False)
    show = db.relationship('Reservation', backref='show', lazy=True)


class Theatre(db.Model):
    __tablename__ = 'theatre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

