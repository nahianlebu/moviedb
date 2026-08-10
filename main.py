import os

import pymysql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DB = dict(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASS", "hello world"),
    database="movielab",
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor,
)


def q(sql, args=()):
    with pymysql.connect(**DB) as con, con.cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchall()


def one(sql, args=()):
    with pymysql.connect(**DB) as con, con.cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchone()


@app.route("/")
def index():
    s = request.args.get("q", "")
    movies = q(
        """SELECT m.movieID, m.title, m.genre, m.director, m.releaseYear,
                         ROUND(AVG(r.rating),1) AS avg_rating
                  FROM movies m LEFT JOIN ratings r ON m.movieID = r.movieID
                  WHERE m.title LIKE %s OR m.genre LIKE %s OR m.director LIKE %s
                  GROUP BY m.movieID ORDER BY m.releaseYear DESC""",
        (f"%{s}%",) * 3,
    )
    return render_template("index.html", movies=movies, q=s)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with pymysql.connect(**DB) as con, con.cursor() as cur:
            cur.execute(
                "INSERT INTO movies (title,genre,director,releaseYear) VALUES (%s,%s,%s,%s)",
                (
                    request.form["title"],
                    request.form["genre"],
                    request.form["director"],
                    request.form["year"],
                ),
            )
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/movie/<int:mid>")
def movie(mid):
    m = one(
        """SELECT m.*, ROUND(AVG(r.rating),1) AS avg_rating
               FROM movies m LEFT JOIN ratings r ON m.movieID = r.movieID
               WHERE m.movieID = %s GROUP BY m.movieID""",
        (mid,),
    )
    ratings = q("SELECT * FROM ratings WHERE movieID=%s ORDER BY ratingID DESC", (mid,))
    return render_template("movie.html", m=m, ratings=ratings)


@app.route("/rate/<int:mid>", methods=["POST"])
def rate(mid):
    f = request.form
    with pymysql.connect(**DB) as con, con.cursor() as cur:
        cur.execute(
            """INSERT INTO ratings (movieID,story,acting,visual,sound,direction)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
            (mid, f["story"], f["acting"], f["visual"], f["sound"], f["direction"]),
        )
    return redirect(url_for("movie", mid=mid))


@app.route("/delete/<int:mid>", methods=["POST"])
def delete(mid):
    with pymysql.connect(**DB) as con, con.cursor() as cur:
        cur.execute("DELETE FROM movies WHERE movieID=%s", (mid,))
    return redirect(url_for("index"))


@app.route("/delete_rating/<int:rid>", methods=["POST"])
def delete_rating(rid):
    mid = request.form["mid"]
    with pymysql.connect(**DB) as con, con.cursor() as cur:
        cur.execute("DELETE FROM ratings WHERE ratingID=%s", (rid,))
    return redirect(url_for("movie", mid=mid))


@app.route("/top")
def top():
    return render_template("top.html", rows=q("SELECT * FROM top_movies"))


if __name__ == "__main__":
    app.run(debug=True)
