from app.models import Availability


def save_availability_to_db(data):
    """ Save availability to db """
    availability = Availability(**data)
    availability.save_to_db()

    return availability
