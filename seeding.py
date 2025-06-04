from extensions import db
from models import FitnessClass
from datetime import datetime
from pytz import timezone, utc
from app import create_app

app = create_app()

with app.app_context():
    db.create_all()

    # Adding sample data if not already present
    if not FitnessClass.query.first():
        # Set timezone for IST {ASSUMPTION: All dates are in IST}
        ist = timezone('Asia/Kolkata')

        # funtion to convert IST string -> UTC datetime
        def to_utc(dt_str):
            local_dt = ist.localize(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))
            return local_dt.astimezone(utc)

        class1 = FitnessClass(
            name="Yoga",
            instructor="John",
            date=to_utc("2025-06-10 10:00"),
            available_slots=5,
            max_slots=20
        )
        class2 = FitnessClass(
            name="Zumba",
            instructor="Jane",
            date=to_utc("2025-06-11 11:00"),
            available_slots=3,
            max_slots=10
        )
        class3 = FitnessClass(
            name="HIIT",
            instructor="Tony",
            date=to_utc("2025-03-11 11:00"),
            available_slots=4,
            max_slots=20
        )

        db.session.add_all([class1, class2, class3])
        db.session.commit()
