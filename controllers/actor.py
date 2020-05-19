from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.movie import Movie
from models.actor import Actor
from settings.constants import ACTOR_FIELDS, DATE_FORMAT  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    update_data = dict()

    if 'date_of_birth' in data.keys():
        try:
            update_data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
        except:
            err = 'date is inappropriately formated, try %d.%m.%Y, or not existent'
            return make_response(jsonify(error=err), 400)

    for key, value in data:
        if key != 'date_of_birth':
            update_data[key] = value

    new_record = Actor.create(**update_data)
    try:
        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    except:
        err = 'New record is not correct'
        return make_response(jsonify(error=err), 400)

    return make_response(jsonify(new_actor), 200)


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    update_data = {}
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        if 'date_of_birth' in data.keys():
            try:
                update_data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
            except:
                err = 'date is inappropriately formated, try %d.%m.%Y, or not existent'
                return make_response(jsonify(error=err), 400)

        for key, value in data.items():
            if key != 'id' and key != 'date_of_birth':
                update_data[key] = value

        upd_record = Actor.update(row_id, **update_data)
        try:
            upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(upd_actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    ### END CODE HERE ###


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        stat = Actor.delete(row_id)
        if stat == 1:
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
        elif stat == 0:
            err = 'Record not deleted'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
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

            rel_obj = Movie.query.filter_by(id=relation_id).first()
            actor = Actor.add_relation(row_id, rel_obj)
            try:
                rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
                rel_actor['filmography'] = str(actor.filmography)
            except:
                err = 'Error while add relation'
                return make_response(jsonify(error=err), 400)

            return make_response(jsonify(rel_actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def actor_clear_relations():
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

        actor = Actor.clear_relations(row_id)
        try:
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
        except:
            err = 'Error while clear relation'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(rel_actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

#
# def delete_all_actors():
#     return Actor.delete_all()