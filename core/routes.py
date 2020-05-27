from flask import current_app as app
from flask import request, Response, render_template, flash, redirect, url_for
from sqlalchemy import func
import pandas as pd
import numpy as np

from controllers.movie import *
from models.users import *
from settings.constants import *


# Set "homepage" to index.html
# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        same_email = Data.query.filter_by(email=email).first()
        same_phone = Data.query.filter_by(phone=phone).first()
        if same_email is not None:
            flash(u"User with such email already exist", "warning")
            return redirect(url_for('Index'))

        if same_phone is not None:
            flash(u"User with such phone already exist", "warning")
            return redirect(url_for('Index'))

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully", "success")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully", "success")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully", "success")

    return redirect(url_for('Index'))


# this route is for inserting data to mysql database via html forms
@app.route('/movies/<user_id>/', methods=['GET'])
def get_movies(user_id):
    all_data = Movie.query.filter_by(user_id=user_id).all()

    return render_template("movies.html", movies=all_data, user_id=user_id)


# this route is for inserting data to mysql database via html forms
@app.route('/insert_movie/<user_id>', methods=['POST'])
def insert_movie(user_id):
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        genre = request.form['genre']
        rating = request.form['rating']
        review = request.form['review']

        obj = Movie.query.filter_by(user_id=user_id, name=name).first()
        if obj is not None:
            flash(u"Movies with this name already exist", "warning")

            return redirect(url_for('get_movies', user_id=user_id))

        if len(review) > 50:
            flash(f"Too big review, length is {len(review)}, but must be <50", "warning")

            return redirect(url_for('get_movies', user_id=user_id))

        my_data = Movie(name, year, genre, rating, review, user_id)
        db.session.add(my_data)
        db.session.commit()

        flash("Movies Inserted Successfully", "success")

        return redirect(url_for('get_movies', user_id=user_id))


# this is our update route where we are going to update our employee
@app.route('/update_movie/<user_id>', methods=['GET', 'POST'])
def update_movie(user_id):
    if request.method == 'POST':
        my_data = Movie.query.get(request.form.get('id'))

        obj = Movie.query.filter_by(name=my_data.name).first()

        my_data.name = request.form['name']
        my_data.year = request.form['year']
        my_data.genre = request.form['genre']
        my_data.rating = request.form['rating']
        my_data.review = request.form['review']
        my_data.user_id = user_id

        db.session.commit()
        flash("Movie Updated Successfully", "success")

        return redirect(url_for('get_movies', user_id=user_id))


# This route is for deleting our employee
@app.route('/delete_movie/<id>/<user_id>', methods=['GET', 'POST'])
def delete_movie(id, user_id):
    my_data = Movie.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Movies Deleted Successfully", "success")

    return redirect(url_for('get_movies', user_id=user_id))


labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]


@app.route('/bar')
def bar():
    query = db.select([db.func.avg(Movie.rating).label('avg_rating'), Movie.name]).group_by(Movie.name)
    my_data = db.engine.execute(query).fetchall()
    df = pd.DataFrame(my_data)
    bar_values = np.round(df.loc[:, 0].to_numpy(dtype=float), 2).tolist()
    bar_labels = df.loc[:, 1].tolist()
    return render_template('bar_chart.html', title='Raiting', max=6, labels=bar_labels, values=bar_values)


def get_average_rating(self):
    some = db.select([db.func.avg(Movie.columns.rating).label('avg_rating'), Movie.columns.name]).group_by(Movie.columns.name)
    print(some)

    avg = db.session.query(func.avg(Movie.rating)).scalar()
    if avg is not None:
        avg = round(avg, 2)
    return avg








