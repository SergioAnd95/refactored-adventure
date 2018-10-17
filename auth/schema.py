from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length, Regexp

from core.db import db

# from webargs import fields, ValidationError


from .models import User


def unique_validation(model, field):
    """
    Unique validation for model field
    :param model: db.Model
    :param field: db.Column
    :return: def
    """

    async def wrapper(data):
        instance = await model.query.where(field == data).gino.first()
        if instance:
            raise ValidationError('%s with this %s already exist' % (model.__name__, field.name))

    return wrapper


class RegistrationRequestSchema(Schema):
    email = fields.Email(required=True, validate=[unique_validation(User, User.email)])
    password = fields.Str(required=True, validate=[Length(min=7), Regexp(r'[a-zA-z0-9]+')])


class LoginRequestSchema(Schema):
    email = fields.Email(required=True, validate=[Length(min=1)])
    password = fields.Str(required=True, validate=[Length(min=1)])


class FacebookLoginSchema(Schema):
    token = fields.Str(required=True, description='facebook user access token', validate=[Length(min=1)])