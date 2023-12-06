from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
migrate = Migrate()


class Base(db.Model):
    """ Model that contains base database models. """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save_to_db(self):
        """ Saving into db """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        """  Updating into db """
        for key, value in kwargs.items():
            setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_from_db(self):
        """ Deleting from database """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        """ Find by id """
        return cls.query.filter_by(id=id).first()


class User(Base):
    __tablename__ = 'user'
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    w_real = db.Column(db.Integer, nullable=True)
    is_disabled = db.Column(db.Boolean, default=False)
    shift = db.relationship("Shift", cascade="delete")
    forecast = db.relationship("Forecast", cascade="delete")
    availability = db.relationship("Availability", cascade="delete")

    def serialize(self):
        """ Return the user data """
        return {
            "id": self.id,
            "email": self.email,
            "is_disabled": self.is_disabled,
            "w_real": self.w_real,
        }

    def set_password(self, password):
        """ Setting password for user """
        self.password = generate_password_hash(password)

    def set_email_lower(self, email):
        """Setting the lowercase email"""
        self.email = email.lower()

    def check_password(self, password):
        """ Checking password for user """
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        """ Find user by email address """
        email_lower = email.lower()
        return cls.query.filter_by(email=email_lower).first()

    @staticmethod
    def exists(email):
        """ Check if user exists """
        email_lower = email.lower()
        user = User.find_by_email(email_lower)
        if user:
            return True
        return False


class Shift(Base):
    __tablename__ = 'shift'
    name = db.Column(db.String(50), unique=True, nullable=False)
    start_shift = db.Column(db.String(255), nullable=False)
    end_shift = db.Column(db.String(255), nullable=False)
    shift_type = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        """ Return the user data """
        return {
            "id": self.id,
            "name": self.name,
            "start_shift": self.start_shift,
            "end_shift": self.end_shift,
            "shift_type": self.shift_type,
            "user_id": self.user_id,
        }

    @staticmethod
    def find_all_by_user_id(user_id):
        """ Find user by email address """
        return Shift.query.filter_by(user_id=user_id).all()


class Forecast(Base):
    __tablename__ = 'forecast'
    date = db.Column(db.String(50), unique=True, nullable=False)
    demand = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        """ Return the user data """
        return {
            "date": self.date,
            "demand": self.demand
        }

    @staticmethod
    def find_all_by_user_id(user_id):
        """ Find user by email address """
        return Forecast.query.filter_by(user_id=user_id).all()


class Availability(Base):
    __tablename__ = 'availability'
    collaborator = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    is_available = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        """ Return the user data """
        return {
            "collaborator": self.dacollaboratorte,
            "date": self.date,
            "is_available": self.is_available,
            "week": self.week,
            "day": self.day,
            "user_id": self.user_id,
            }

    @staticmethod
    def find_all_by_user_id(user_id):
        """ Find user by email address """
        return Availability.query.filter_by(user_id=user_id).all()
