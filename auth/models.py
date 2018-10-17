from core.db import db

from passlib.hash import pbkdf2_sha256


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String())
    email = db.Column(db.String(128), nullable=False, unique=True)
    first_name = db.Column(db.Unicode(30))
    last_name = db.Column(db.Unicode(30))
    facebook_id = db.Column(db.Unicode(256))

    def password_match(self, input_password):
        return pbkdf2_sha256.verify(input_password, self.password)
