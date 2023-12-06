import unittest
from app.models import Shift
from tests import BaseTestCase
from tests.utils.user import save_user_to_db
from tests.utils.shift import save_shift_to_db
from app.schemas import ShiftSchema


shift_schema = ShiftSchema()


class TestShiftModel(BaseTestCase):
    """Test that shift model is ok"""

    def setUp(self):
        """Setting up the test class"""
        super().setUp()
        self.user_data = {
            "email": "example@mail.com",
            "password": "123456"
        }
        self.shift_data = {
            "name": "madrugada FT",
            "start_shift": "0:00",
            "end_shift": "8:00",
            "shift_type": "mañana",
            "user_id": 1,
        }
        save_user_to_db(self.user_data)

    def test_shift_representation(self):
        """ Test string representation of shift model """
        name = self.shift_data.get("name", None)
        start_shift = self.shift_data.get("start_shift", None)
        end_shift = self.shift_data.get("end_shift", None)
        shift_type = self.shift_data.get("shift_type", None)
        shift = shift_schema.load(self.shift_data)
        self.assertEqual(name, shift['name'])
        self.assertEqual(start_shift, shift['start_shift'])
        self.assertEqual(end_shift, shift['end_shift'])
        self.assertEqual(shift_type, shift['shift_type'])

    def test_create_success(self):
        """ Test create shift is success """
        shift = save_shift_to_db(self.shift_data)
        self.assertIsNotNone(shift.id)
        for key in self.shift_data.keys():
            self.assertEqual(
                getattr(shift, key), self.shift_data.get(key, None)
            )
