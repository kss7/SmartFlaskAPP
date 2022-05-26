from flask import jsonify, request, Blueprint
import json
from flask_login import login_user, current_user, login_required, logout_user
from main.models import User, UserSchema
from main import db
blueprint = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

############## routes #################
@blueprint.route('/', methods=['GET', 'POST'])
def index():
    #if 'email' in session:
    #    username = session['email']
    #   return jsonify({'message': 'You are already logged in', 'username': username})
    #else:
        resp = jsonify({'message': 'Unauthorized access, please login'})
        resp.status_code = 401
        return resp


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    info = json.loads(request.data)
    email = info.get('email')
    password = info.get('password')
    user = User(email, password)
    user_email = User.query.filter_by(email=email).first()
    if user_email:
        return jsonify({"status": 422,
                 "msg": "Username or Password Exists"}), 422
    else:
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify(user.to_json()), 201


@blueprint.route('/login', methods=['POST'])
def login():
        password = request.json['password']
        email = request.json['email']
        user = User.query.filter_by(email=email).first()
        if user and user.is_correct_password(password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return jsonify({"status": 200, "msg": user.email + " logged in", "userId": str(user.id)})
        else:
            return jsonify({"status": 401,
                            "reason": "Username or Password not exists"}), 401


@blueprint.route("/authuserscount", methods=["GET"])
def get_auth_users():
    auth_users = User.get_auth_user_count()
    return jsonify({"count": auth_users})


@blueprint.route("/users", methods=["GET"])
def get_all_users():
    result = users_schema.dump(User.get_all_users())
    return jsonify({"users":result})


@blueprint.route("/allusercount", methods=["GET"])
def get_all_users_count():
    allusers = User.get_all_users_count()
    print (allusers)
    return jsonify({"count": allusers})


@blueprint.route("/checkusers", methods=["GET"])
def check_total_employee(auth=None, all=None):
    auth_count = auth or User.get_auth_user_count()
    all_count = all or User.get_all_users_count()
    if auth_count > 100:
        return jsonify({"auth_count": auth_count, "all_count":all_count,
                            "msg": "Error! Auth emp count is more than employees"})
    elif auth_count < all_count:
        percent = int((auth_count/all_count)*100)
        if percent < 95:
            return jsonify({"auth_count": auth_count, "all_count":all_count,
                            "msg": "Percentage of joining is too less"})
        else:
            return jsonify({"auth_count": auth_count, "all_count": all_count,
                            "msg": "Percentage of joining is OK"})
    else:
        return jsonify({"auth_count": auth_count, "all_count": all_count,
                            "msg": "All good"})


@blueprint.route('/logout')
def logout():
    pass
    #user = current_user
    #user.authenticated = False
    #logout_user()


@blueprint.route('/delete', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    uid = record.get('id')
    user = User.query.filter_by(id=uid).first()
    if not user:
        return jsonify({'error': 'data not found'}), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.to_json())