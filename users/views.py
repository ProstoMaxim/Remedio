from flask import jsonify
from models import Users, db
from flask_project import app
from flask import request
from sqlalchemy import func

ATTRIBUTES = ['id', 'name', 'birthdate', 'account_value', 'state', 'address', 'hiredate']

def get_user(user):
    return {attr:getattr(user, attr) for attr in ATTRIBUTES}


def add_user(user, parameters):

    for attr in parameters:
        if attr in ATTRIBUTES:
            setattr(user, attr, request.args[attr])
        else:
            print 'Could not change '+attr+': user table have no such attribute!'


@app.route('/users/list')
def list_all():

    users = Users.query.all()
    users_list = [get_user(user) for user in users]

    return jsonify({"data": users_list})


@app.route('/users/save')
def save_user():

    user_id = request.args.get('id')
    result = 'failure'

    try:

        if user_id:
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                user = Users()
                db.session.add(user)
        else:
            user = Users()
            db.session.add(user)

        add_user(user, request.args)
        db.session.commit()
        result = 'success'
        user_dict = get_user(user)

    except Exception as e:

        print 'Could not save user:'
        print e
        user_dist = None

    return jsonify({"data": user_dict, "result": result})


@app.route('/count')
def get_attribute_count():

    VALID_PARAMETERS = ('state', 'hire_date')
    parameter = request.args.get('group_by')
    result = 'failure'
    data_list = list()

    if parameter not in VALID_PARAMETERS:
        print 'Invalid sorting parameter! Expecting one of following:', VALID_PARAMETERS
        return jsonify({"data": None, "result": result})

    try:
        query = db.session.query(parameter, func.count(Users.id)).group_by(parameter).all()

    except Exception as e:
        print 'Could not query database:'
        print e
        return jsonify({"data": None, "result": result})

    for row in query:
        data = {}
        data.update({parameter: row[0]})
        data.update({"count": row[1]})
        data_list.append(data)


    return jsonify({"data": data_list, "result": result})

