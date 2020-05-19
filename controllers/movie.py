from flask import jsonify, make_response

from ast import literal_eval

from models.movie import Movie
from models.actor import Actor
from settings.constants import MOVIE_FIELDS, DATE_FORMAT
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        act = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(act)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    if 'year' in data.keys():
        try:
            data['year'] = int(data['year'])
        except:
            err = 'Year must be integer'
            return make_response(jsonify(error=err), 400)

    new_record = Movie.create(**data)
    try:
        new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
    except:
        err = 'New record is not correct'
        return make_response(jsonify(error=err), 400)

    return make_response(jsonify(new_movie), 200)


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()

    if 'year' in data.keys():
        try:
            data['year'] = int(data['year'])
        except:
            err = 'Year must be integer'
            return make_response(jsonify(error=err), 400)

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        upd_record = Movie.update(row_id, **data)
        try:
            upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(upd_movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        stat = Movie.delete(row_id)
        if stat == 1:
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
        elif stat == 0:
            err = 'Record not deleted'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        if 'relation_id' in data.keys():
            try:
                relation_id = int(data['id'])
            except:
                err = 'Relation id must be integer'
                return make_response(jsonify(error=err), 400)

            rel_obj = Actor.query.filter_by(id=relation_id).first()
            movie = Movie.add_relation(row_id, rel_obj)
            try:
                rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
                rel_movie['cast'] = str(movie.cast)
            except:
                err = 'Error while add relation'
                return make_response(jsonify(error=err), 400)

            return make_response(jsonify(rel_movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        movie = Movie.clear_relations(row_id)
        try:
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
        except:
            err = 'Error while clear relation'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(rel_movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

#
# def delete_all_movies():
#     return Movie.delete_all()
