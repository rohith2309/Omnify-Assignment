
from datetime import datetime
from extensions import db



class FitnessClass(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    instructor = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    max_slots = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(80), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    fitness_class_id = db.Column(db.Integer, db.ForeignKey('fitness_class.id'), nullable=False)
    fitness_class = db.relationship('FitnessClass', backref=db.backref('bookings', lazy=True))