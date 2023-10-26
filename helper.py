import imdb
import requests
import sqlite3
from flask import Flask, g

app = Flask(__name__)

# a class constructor that creates an instance of the IMDb
  # class provided by the imdb module in Python.
ia = imdb.IMDb()

# Get the top 100 movies by rating
top250 = ia.get_top250_movies()

# Iterate over the top 100 movies and print their titles and ratings
#for i in range(100,101):
#    movie = ia.get_movie(top250[i].getID())
#    print(f"{movie['title']} ({movie['year']}): {movie['rating']} <{movie['poster']}>")


DATABASE = 'inamovies.db'
def get_db():
    """Get a new database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db
with app.app_context():
    db = get_db()
    cur = db.cursor()
    for i in range(98):
        # get the IMDb movie object for the current movie
        movie = ia.get_movie(top250[i].getID())

        # use the OMDB API to get additional information about the movie
        omdb_url = f"http://www.omdbapi.com/?t={movie['title']}&y={movie['year']}&apikey=393367aa"
        omdb_response = requests.get(omdb_url)
        omdb_data = omdb_response.json()
        #print(omdb_data)
        # get the title and poster from the OMDB response
        title = omdb_data['Title']
        poster = omdb_data['Poster']
        year = omdb_data['Year']
        category = omdb_data['Rated']
        duration = omdb_data['Runtime']
        desc = omdb_data['Plot']
        rating = omdb_data['Ratings'][0]['Value']
        language = omdb_data['Language']
        genre = omdb_data['Genre']
        try:
            cur.execute("INSERT INTO movies (title, year, rating, category, duration, poster, desc, language, genre) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, year, rating, category, duration, poster, desc, language, genre))
            db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()

