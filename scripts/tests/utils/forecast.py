from app.models import Forecast


def save_forecast_to_db(data):
    """ Save forecast to db """
    forecast = Forecast(**data)
    forecast.save_to_db()

    return forecast