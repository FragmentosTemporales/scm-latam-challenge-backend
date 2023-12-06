from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema
from app.models import User, Shift, Forecast, Availability


ma = Marshmallow()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

    password = auto_field(load_only=True)


class LoginSchema(ma.Schema):
    """ Serializer for logs users in """
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El campo de correo es requerido.",
            "null": "Este campo de correo no debe estar vacío.",
            "validator_failed": "El correo ingresado no es válido.",
            "invalid": "El valor ingresado no es un correo electrónico válido."
        }
    )
    password = fields.String(
        required=True,
        error_messages={
            "required": "El campo de password es requerido.",
            "null": "Este campo de password no debe estar vacío.",
            "validator_failed": "La password ingresada no es válida.",
            "invalid": "El valor ingresado no es una contraseña válida."
        }
    )


class ShiftSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Shift
        include_relationships = True

    user_id = auto_field(required=True)


class AvailabilitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Availability
        include_relationships = True

    user_id = auto_field(required=True)


class ForecastSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Forecast
        include_relationships = True

    user_id = auto_field(required=True)
