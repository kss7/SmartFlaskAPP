from main import db, bcrypt
from datetime import datetime
from marshmallow import fields, Schema, validate
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.LargeBinary(80), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')

    def __init__(self, email, plaintext_password, role='user'):
        self.email = email
        self.hashed_password = bcrypt.generate_password_hash(plaintext_password)
        self.authenticated = False
        self.registered_on = datetime.now()
        self.role = role

    def set_password(self, plaintext_password):
        self.hashed_password = bcrypt.generate_password_hash(plaintext_password)

    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.hashed_password, plaintext_password)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    #@property
    #def is_anonymous(self):
    #    return False

    def get_id(self):
        return str(self.id)

    def get_email(self):
        return str(format(self.email))

    def get_role(self):
        return str(format(self.role))

    def to_json(self):
        return {"id": format(self.id),
                "email": format(self.email)}

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_all_users_count():
        return User.query.count()

    @staticmethod
    def get_auth_user_count():
        return User.query.filter_by(authenticated=1).count()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return '<User {}>'.format(self.email)


# class UserSchema(Schema):
#     id = fields.Int(dump_only=True)
#     email = fields.Email(required=True, validate=validate.Email(error="Invalid email address provided"))
#     hashed_password = fields.Str(required=True, validate=[validate.Length(min=2, max=8)])
#     registered_on = fields.DateTime(dump_only=True)
#     modified_at = fields.DateTime(dump_only=True)
#     authenticated = fields.Boolean(dump_only=True)

class UserSchema(Schema):
    class Meta:
        #exposed fields
        fields = ('id', 'email', 'registered_on', 'authenticated')


