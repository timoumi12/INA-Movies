import sqlite3
import os
from flask import Flask, flash, redirect, render_template, request, jsonify, g
from flask_session import Session

app = Flask(__name__)
DATABASE = 'topmovies.db'

def get_db():
    """Get a new database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.before_request
def before_request():
    """Get a new database connection before each request."""
    g.db = get_db()
    g.cursor = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    """Close the database connection after each request."""
    db = g.pop('db', None)
    if db is not None:
        db.commit()
        db.close()

def test():
    db = get_db()
    cur = db.cursor()
    query = "select * from movies"
    cur.execute