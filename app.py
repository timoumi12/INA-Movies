import os
from flask import Flask, flash, redirect, render_template, request, jsonify, g, url_for, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
#from helper import apology, login_required, lookup
import sqlite3
import itertools
from functools import wraps

app = Flask(__name__)
app.jinja_env.auto_reload = True


DATABASE = 'inamovies.db'

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


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def dblookup(d):
    #print("haha",d)
    data = []
    for row in d:
        data.append({
            'title': row[0],
            'year': row[1],
            'rating': row[2],
            'category': row[3],
            'duration': row[4],
            'poster': row[5],
            'desc': row[6],
            'id': row[7]
        })
    return data
#conn = sqlite3.connect('topmovies.db')

@app.route('/', methods = ["POST","GET"])
def mainpage():
    return render_template("homepage.html")

@app.route('/duplicate', methods = ["POST","GET"])
@login_required
def sndHP():
    return render_template('duplicate.html', username=session['user_id'])

cache = {}


@app.route('/login', methods = ["POST","GET"])
def login():
    session.clear()
    check = 1
    if request.method == "POST":
        if request.form.get("username") and request.form.get("pwd"):
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
            data = []
            d = cur.fetchall()
            print(request.form.get("username"))
            print(d)
            if len(d) != 1 or not check_password_hash(d[0][2], request.form.get("pwd")):
                check = 0
                return render_template("login.html", check = check, msg = "Incorrect Username or Password")
            print(data)
            data.append({'id':d[0][0], 'username':d[0][1], 'pwdhash':d[0][2]})
            # Remember which user has logged in
            session["user_id"] = request.form.get("username")
            return redirect(url_for('sndHP', username=request.form.get("username")))
    return render_template("login.html", check=check)

@app.route('/logout', methods = ["POST","GET"])
def logout():
    session.clear()
    return redirect("/")

@app.route('/news', methods = ["POST","GET"])
@login_required
def news():
    return render_template("news.html", username=session['user_id'])

@app.route('/signup', methods = ["POST","GET"])
def signup():
    check = 1
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        #useless
        pwdagain = request.form.get("confpwd")
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        data = cur.fetchall()
        if len(data) != 0 or not username:
            check = 0
            return render_template("signup.html", check=check, msg="Username Already In use")
        cur.execute("INSERT INTO users(username,pwdhash) VALUES (?, ?)", (username, generate_password_hash(pwd),))
        return redirect("/login")
    return render_template("signup.html",check=check)

@app.route('/aboutus', methods = ["POST","GET"])
def abtus():
    return render_template("aboutus.html")

@app.route('/trending', methods = ["POST","GET"])
@login_required
def mainMovies():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(year) FROM movies ORDER BY year ASC")
    y = cur.fetchall()
    years = []
    for row in y:
        years.append({'year' : row[0]})
    cur.execute("SELECT * FROM trendings")
    d = cur.fetchall()
    data = []
    for row in d:
        data.append({
            'id': row[0],
            'title': row[1],
            'trailer': row[2],
            'year': row[3],
            'rating': row[4],
            'duration': row[5],
            'class': row[6],
            'genre': row[7],
            'poster': row[8],
            'category': row[9]
        })
    chunk_size = 3
    grouped_data = list(itertools.zip_longest(*[iter(data)] * chunk_size, fillvalue=None))
    print(grouped_data)
    return render_template("trendingMain.html", years=years, data=data, rows=grouped_data)

@app.route('/searchres', methods = ["POST","GET"])
@login_required
def filter():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(year) FROM movies ORDER BY year ASC")
    y = cur.fetchall()
    years = []
    for row in y:
        years.append({'year' : row[0]})
    if request.method == "POST":
        genre = request.form.get('genre')
        language = request.form.get('language')
        year = request.form.get('year')
        _class = request.form.get('class')
        query = "SELECT * FROM movies WHERE 1=1"
        params = []
        if year:
            query += " AND year = ?"
            params.append(year)
        if _class:
            query += " AND category = ?"
            params.append(_class)
        if genre:
            query += " AND genre LIKE ?"
            params.append('%' + genre + '%')
        if language:
            query += " AND language LIKE ?"
            params.append('%' + language + '%')
        #print("Final query: ", final_query % tuple(params.values()))
        #print(query)
        d = tuple(params)
        #print(d)
        cur.execute(query, d)
        d = cur.fetchall()
        #print(data)
        #print(query)
        #print(data)
        data = []
        for row in d:
            data.append({
                'id': row[0],
                'title': row[1],
                'year': row[2],
                'rating': row[3],
                'category': row[4],
                'duration': row[5],
                'poster': row[6],
                'desc': row[7],
                'language': row[8],
                'genre': row[9]
            })
        return render_template("searchRes.html", data=data, years=years)
    '''cur.execute("SELECT DISTINCT(category) FROM movies")
    categories = dblookup(cur.fetchall())'''
    return render_template("searchRes.html", years=years)


@app.route('/topmovies', methods = ["POST","GET"])
@login_required
def topmovies():
    print(request.form.get("search"))
    db = get_db()
    cur = db.cursor()
    #cur = g.cur
    if request.method == "POST":
        search = request.form.get("search")
        if search:
            if search not in cache:
                db = get_db()
                cur = db.cursor()
                #cur = g.cur
                cur.execute("select title,year,rating,category,duration,poster,desc,id from movies where title like ?", ('%' + search + '%',))
                d=cur.fetchall()
                data = dblookup(d)
                cache[search] = data
            else:
                data = cache[search]
            return render_template("topMovies.html", data = data)
            # Cache the new data
    #I think there's no need to cache the data since it's always the same infos that are going to be displayed
    cur.execute('SELECT title, year, rating, category, duration, poster, desc, id FROM movies;')
    d=cur.fetchall()
    #print("haha",d)
    data = dblookup(d)
    #print("hahaha",data)
    #d = cur.fetchall()
    #data = []
    #for row in d:
    #    data = {'title': row[0], 'year': row[1], 'rating': row[2], 'category': row[3], 'duration': row[4], 'poster': row[5], 'desc': row[6]}
    return render_template("topMovies.html", data = data)




