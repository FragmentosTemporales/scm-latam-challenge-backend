from app.models import Shift


def save_shift_to_db(data):
    """ Save shift to db """
    shift = Shift(**data)
    shift.save_to_db()

    return shift
