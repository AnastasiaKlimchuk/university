from flask import current_app as app
from flask import request, Response, render_template, flash, redirect, url_for

from controllers.movie import *
from models.users import *


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

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

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
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

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

        my_data = Movie(name, year, genre, user_id)
        db.session.add(my_data)
        db.session.commit()

        flash("Movies Inserted Successfully")

        return redirect(url_for('get_movies', user_id=user_id))


# this is our update route where we are going to update our employee
@app.route('/update_movie/<user_id>', methods=['GET', 'POST'])
def update_movie(user_id):
    if request.method == 'POST':
        my_data = Movie.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.year = request.form['year']
        my_data.genre = request.form['genre']
        my_data.user_id = user_id

        db.session.commit()
        flash("Movie Updated Successfully")

        return redirect(url_for('get_movies', user_id=user_id))


# This route is for deleting our employee
@app.route('/delete_movie/<id>/<user_id>', methods=['GET', 'POST'])
def delete_movie(id, user_id):
    my_data = Movie.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Movies Deleted Successfully")

    return redirect(url_for('get_movies', user_id=user_id))
#
# @app.route('/api/actors', methods=['GET'])
# def actors():
#     """
#     Get all actors in db
#     """
#     return get_all_actors()


# @app.route('/api/movies', methods=['GET'])
# def movies():
#     """
#     Get all actors in db
#     """
#     return get_all_movies()


# @app.route('/api/actor', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def actor():
#     if request.method == 'GET':
#         return get_actor_by_id()
#
#     elif request.method == 'POST':
#         return add_actor()
#
#     elif request.method == 'PUT':
#         return update_actor()
#
#     elif request.method == 'DELETE':
#         return delete_actor()


# @app.route('/api/movie', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def movie():
#     if request.method == 'GET':
#         return get_movie_by_id()
#
#     elif request.method == 'POST':
#         return add_movie()
#
#     elif request.method == 'PUT':
#         return update_movie()
#
#     elif request.method == 'DELETE':
#         return delete_movie()

#
# @app.route('/api/actor-relations', methods=['PUT', 'DELETE'])
# def actor_relations():
#
#     if request.method == 'PUT':
#         return actor_add_relation()
#
#     elif request.method == 'DELETE':
#         return actor_clear_relations()

#
# @app.route('/api/movie-relations', methods=['PUT', 'DELETE'])
# def movie_relations():
#
#     if request.method == 'PUT':
#         return movie_add_relation()
#
#     elif request.method == 'DELETE':
#         return movie_clear_relations()


# @app.route("/delete_all_actors")
# def delete_all_act():
#     try:
#         db.session.query(Actor).delete()
#         db.session.commit()
#         return Response('All actors was deleted haha', status=201)
#     except Exception as e:
#         return(str(e))
#
#
# @app.route("/delete_all_movies")
# def delete_all_mov():
#     try:
#         db.session.query(Movie).delete()
#         db.session.commit()
#         return Response('All movies was deleted haha', status=201)
#     except Exception as e:
#         return(str(e))





