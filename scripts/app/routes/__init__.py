import logging
from flask import Blueprint, jsonify, request, send_file
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from app.models import User, Shift, Forecast, Availability
from app.schemas import UserSchema, LoginSchema, ShiftSchema, ForecastSchema, AvailabilitySchema
from app.utils import Set_Availability


main = Blueprint("main", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})


user_schema = UserSchema()
login_schema = LoginSchema()
shift_schema = ShiftSchema()
shifts_schema = ShiftSchema(many=True)
forecast_schema = ForecastSchema()
forecasts_schema = ForecastSchema(many=True)
availabilities_schema = AvailabilitySchema(many=True)


@main.route("/")
def home():
    """ Home function """
    return send_file('../static/index.html'), 200


@main.route("/register", methods=["POST"])
def create_user():
    """Recibe parámetros a través de la consulta y crea el usuario."""
    try:
        args_json = request.get_json()
        try:
            args = user_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            user_exists = User.exists(email)

            if user_exists:
                return jsonify("Usuario ya existe"), 400

            user = User(**args)
            user.set_password(password)
            user.set_email_lower(email)
            user.save_to_db()
            return jsonify("Usuario creado con éxito!"), 201

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/login", methods=["POST"])
def login_user():
    """Recibe parámetros a través de la consulta y retorna un token"""
    try:
        args_json = request.get_json()
        try:
            args = login_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            user = User.find_by_email(email)

            if user is None or \
               user.check_password(password) == False:
                return jsonify("ERROR DE USUARIO O CONTRASEÑA"), 400

            access_token = create_access_token(email)
            user.is_disabled = False
            user.save_to_db()

            return jsonify(
                    {
                        "token": access_token,
                        "user": user_schema.dump(user),
                        "email": user.email,
                        "user_id": user.id,
                    }
            ), 200
    except Exception as e:
        error_message = str(e)
        print(e)
        logging.error(f"Error en login_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/user/<int:user_id>")
def get_user(user_id):
    """Retorna la información del usuario según su ID"""
    try:
        user = User.find_by_id(user_id)
        if user:
            print(user)
            return jsonify(user_schema.dump(user))

        return jsonify("Usuario no encontrado"), 404

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_user: {error_message}")
        return jsonify("ERROR"), 500


# TODO = Validar uso de get_jwt_identity()
@main.route("/userlist/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(id):
    """Recibe parámetros para actualizar o deshabilitar al usuario"""
    try:
        user = User.find_by_id(id)
        uid = get_jwt_identity()
        print(uid)
        if user is None:
            return jsonify(f"Usuario con ID #{id} no encontrado."), 404
        if request.method == "DELETE":
            user.is_disabled = True
            user.save_to_db()
            return jsonify("USUARIO DESHABILITADO"), 204
        user.w_real = request.json.get("w_real")
        user.save_to_db()
        return jsonify("USUARIO ACTUALIZADO"), 200
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en update_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/shift", methods=["POST"])
def create_shift():
    """Recibe parámetros a través de la consulta y crea el horario."""
    try:
        args_json = request.get_json()
        try:
            args = shift_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            if not args:
                return jsonify("empty body."), 400
            Shift(**args).save_to_db()
            return jsonify("successfully!."), 200
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/shift/<int:user_id>", methods=["GET"])
def get_shifts(user_id):
    """Retorna lista de horarios del usuario encontrado por el ID"""
    try:
        shifts = Shift.find_all_by_user_id(user_id)
        if shifts:

            return jsonify(shifts_schema.dump(shifts)), 200

        return jsonify("Horarios no encontrados"), 404
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_shifts: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/forecast", methods=["POST"])
def create_forecast():
    """Recibe parámetros a través de la consulta y crea el horario."""
    try:
        args_json = request.get_json()
        try:
            args = forecast_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            if not args:
                return jsonify("empty body."), 400
            Forecast(**args).save_to_db()
            return jsonify("successfully!."), 200
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/availability/<int:user_id>", methods=["GET"])
def get_availabilities(user_id):
    """ Retorna lista de turnos según ID"""
    try:
        availabilities = Availability.find_all_by_user_id(user_id)
        if availabilities:
            return jsonify(availabilities_schema.dump(availabilities)),200
        return jsonify("Turnos no encontrados"), 404
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_availabilities: {error_message}")
        return jsonify("ERROR"), 500


# TODO = Validar uso de get_jwt_identity()
@main.route("/create/availability/<int:user_id>", methods=["POST"])
def create_availability(user_id):
    """ Crea y retorna lista de turnos """
    try:
        Set_Availability(user_id)
        return jsonify("Turnos creados correctamente"), 200
    
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_availability: {error_message}"), 500
