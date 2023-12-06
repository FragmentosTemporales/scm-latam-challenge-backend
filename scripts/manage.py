import logging
import click
from flask.cli import FlaskGroup
from app import create_app
from app.models import User
from app.utils import Set_Availability
from app.helpers import Installer, Deleter


cli = FlaskGroup(create_app=create_app)


@cli.command("create-user")
@click.option("--email", required=True)
@click.option("--password", required=True)
@click.option("--w_real", required=True)
def create_user(email, password, w_real):
    """ Create user in the platform by command line interface """
    if User.exists(email):
        print("El usuario ya existe en la base de datos")
    try:
        user = User(password=password, email=email, w_real=w_real)
        user.set_password(password)
        user.save_to_db()
        print("Usuario guardado correctamente")
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")


@cli.command("instalar")
def installer_app():
    """ Create data in the platform by command line interface """
    try:
        Installer()
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en installer_app: {error_message}")


@cli.command("prueba")
def testing_app():
    """ Create availability in the platform by command line interface """
    try:
        Set_Availability(1)
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en testing_app: {error_message}")


@cli.command("eliminar")
def deleter_app():
    """ Create data in the platform by command line interface """
    try:
        Deleter()
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en deleter_app: {error_message}")


@cli.command("test")
@click.option("--test_name")
def test(test_name=None):
    """ Runs the unit tests."""
    import unittest
    if test_name is None:
        tests = unittest.TestLoader().discover('tests', pattern="test_*.py")
    else:
        tests = unittest.TestLoader().loadTestsFromName('tests.' + test_name)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    cli()
