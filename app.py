from flask import Flask, request, jsonify
from datetime import datetime, timedelta,UTC
from extensions import db
from models import FitnessClass, Booking
from pytz import timezone, utc


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
app=create_app()




@app.route('/api/create_class', methods=['POST'])
def create_class():
    data = request.get_json()
    
    required_fields = ['name', 'instructor', 'date', 'available_slots', 'max_slots']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        # Parsing date from string input in IST timezone
        ist = timezone('Asia/Kolkata')
        local_dt = ist.localize(datetime.strptime(data['date'], "%Y-%m-%d %H:%M"))
        utc_dt = local_dt.astimezone(utc)
    except Exception as e:
        return jsonify({'error': f'Invalid date format. Use YYYY-MM-DD HH:MM. Error: {str(e)}'}), 400

    new_class = FitnessClass(
        name=data['name'],
        instructor=data['instructor'],
        date=utc_dt,
        available_slots=int(data['available_slots']),
        max_slots=int(data['max_slots'])
    )

    db.session.add(new_class)
    db.session.commit()

    return jsonify({
        'message': 'Class created successfully',
        'class': {
            'id': new_class.id,
            'name': new_class.name,
            'instructor': new_class.instructor,
            'date_utc': new_class.date.strftime('%Y-%m-%d %H:%M'),
            'available_slots': new_class.available_slots,
            'max_slots': new_class.max_slots
        }
    }), 201

@app.route('/', methods=['GET'])
def apis():
    return jsonify({
        'message': 'Welcome to the API',
        'endpoints': {
            '/': 'Home endpoint',
            '/api/classes?tz=TimeZone': 'List all upcoming classes (GET)',
            '/api/book?tz=TimeZone': 'Book a class (POST) required fields[class_id,client_name,client_email]',
            '/api/bookings/<client_email>?tz=TimeZone': 'Get bookings for a client (GET)',
            '/api/create_class': 'Create a new fitness class (POST) required fields[name,instructor,date,available_slots,max_slots]'
            
        }
    })


@app.route('/api/classes', methods=['GET'])
def get_classes():
    tz= request.args.get('tz', 'Asia/Kolkata')  # Default to Asia/Kolkata if not provided
    local_tz = timezone(tz)  # to handle timezone conversion
    
    results=[]
    now= datetime.now()
    classes=FitnessClass.query.filter(FitnessClass.date > now).all()
    if not classes:
        return jsonify({'message': 'No upcoming classes found'}), 404
    for cls in classes:
            results.append({
                'id': cls.id,
                'instructor': cls.instructor,
                'date': cls.date.astimezone(local_tz).strftime('%d-%m-%Y %H:%M'),
                'available_slots': cls.available_slots,
                'max_slots': cls.max_slots,
                'name': cls.name
            })    
    return jsonify(results)


@app.route('/api/book', methods=['POST','GET'])
def book_class():
    tz= request.args.get('tz', 'Asia/Kolkata')  # Default to Asia/Kolkata
    local_tz = timezone(tz)  # to handle timezone conversion
    if request.method=='POST':
        data = request.get_json()
        class_id = data.get('class_id')
        client_name = data.get('client_name')
        client_email = data.get('client_email')

        if not class_id or not client_name or not client_email:
            return jsonify({'error': 'Missing required fields'}), 400
        
        fitness_class = FitnessClass.query.filter_by(id=class_id).first()
        
        if not fitness_class:
            return jsonify({'error': 'Class not found'}), 404
        
        if fitness_class.available_slots <= 0:
            return jsonify({'error': 'No available slots for this class'}), 400
        
        
        
        existing_booking = Booking.query.filter_by(fitness_class_id=class_id, client_email=client_email).first() #preventing duplicate bookings
        print(existing_booking)
        if existing_booking:
           return jsonify({'error': 'You have already booked this class'}), 400
        
        fitness_class.available_slots -= 1
        
        new_booking = Booking(
            
            client_name=client_name,
            client_email=client_email,
            booking_time=datetime.now(UTC),
            fitness_class_id=fitness_class.id
            )
        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message': 'Booking successful', 'class': {
            'id': fitness_class.id,
            'name': fitness_class.name,
            'instructor': fitness_class.instructor,
            'available_slots': fitness_class.available_slots,
            'max_slots': fitness_class.max_slots,
            'date': fitness_class.date.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        }}), 200
                

        
    else:
        return jsonify({
        'message': 'Booking successful',
        'class': {
            'id': fitness_class.id,
            'name': fitness_class.name,
            'available_slots': fitness_class.available_slots,
            'max_slots': fitness_class.max_slots,
            'instructor': fitness_class.instructor,
            'date':fitness_class.date.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        }
    }), 200

@app.route('/api/bookings/', methods=['GET'])
def get_bookings():
    client_email = request.args.get('client_email', '').strip()   
    tz=request.args.get('tz', 'Asia/Kolkata')  # Default to Asia/Kolkata if not provided
    
    local_tz = timezone(tz) #to handle timezone conversion
    if not client_email:
        return jsonify({"error": "Client email is required"}), 400

    client_bookings = db.session.query(Booking, FitnessClass).join(
        FitnessClass,
        Booking.fitness_class_id == FitnessClass.id
    ).filter(
        db.func.lower(Booking.client_email) == db.func.lower(client_email)
    ).all()
    
    

    if not client_bookings:
        return jsonify({"message": "No bookings found for this client"}), 404

    results = []
    for booking, fitness_class in client_bookings:
        results.append({
            "booking_id": booking.id,
            "client_name": booking.client_name,
            "client_email": booking.client_email,
            "booking_time": booking.booking_time.strftime('%d-%m-%Y %H:%M'),
            "class_details": {
                "class_id": fitness_class.id,
                "class_name": fitness_class.name,
                "instructor": fitness_class.instructor,
                "date": fitness_class.date.astimezone(local_tz).strftime('%d-%m-%Y %H:%M'),  # Convert to local timezone
                "available_slots": fitness_class.available_slots
            }
            
        })

    return jsonify(results), 200

    

if __name__ == '__main__':
    app.run(debug=True, port=8000)    