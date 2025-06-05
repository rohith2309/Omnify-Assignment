Steps to be followed in order to run this app.

1. create a virtual python env
2. pip install the modules that are mentioned in requirements.txt
3. activate the virtual env
4. delete the instance folder (to create a new DB)
5. run the seeding.py (to populate the db with sample data)
6. run testsql.py to see the table data

ENDPOINTS (POSTMAN): examples

1.  "/" :- "http://127.0.0.1:8000/" [GET]

    - expected o/p: (retrieves all the endpoints)

    {
    "endpoints": {
    "/": "Home endpoint",
    "/api/book?tz=TimeZone": "Book a class (POST) required fields[class_id,client_name,client_email]",
    "/api/bookings?client_email=client_email?&tz=TimeZone": "Get bookings for a client (GET)",
    "/api/classes?tz=TimeZone": "List all upcoming classes (GET)",
    "/api/create_class": "Create a new fitness class (POST) required fields[name,instructor,date,available_slots,max_slots]"
    },
    "message": "Welcome to the API"
    }

2.  "/api/create_class":- "http://127.0.0.1:8000/api/create_class"[POST]

    -required payload:
    -required_fields = ['name', 'instructor', 'date', 'available_slots', 'max_slots']
    -Creates a class with the above fields.  
     {
    "name":"Yoga",
    "instructor":"Sam",
    "date":"2025-07-05 12:30",
    "available_slots":2,
    "max_slots":10
    }

    -expected o/p:
    {
    "class": {
    "available_slots": 2,
    "date_utc": "2025-07-05 07:00",
    "id": 4,
    "instructor": "Sam",
    "max_slots": 10,
    "name": "Yoga"
    },
    "message": "Class created successfully"
    }

3.  "/api/bookings?client_email=client_email?&tz=TimeZone" :- "http://127.0.0.1:8000/api/bookings?client_email=tony@example.com&tz=ASIA/kolkata" "Get bookings for a client [GET]",

    -expected o/p:

    i) if no bookings available for the provided email id:
    {"message": "No bookings found for this client"}

    ii) if bookings are available :
    List of bookings made by that email id

    -tz is a query parameter which is used to manage appropriate client region, by default it is "ASIA/KOLKATA"

4.  "/api/classes?tz=TimeZone" :- "http://127.0.0.1:8000/api/classes?tz=Asia/Kolkata" "List all upcoming classes [GET]"

    -expected o/p:

    i) if classes available:

         [
        {
         "available_slots": 5,
         "date": "10-06-2025 04:30",
         "id": 1,
         "instructor": "John",
         "max_slots": 20,
         "name": "Yoga"

    },
    {
    "available_slots": 3,
    "date": "11-06-2025 05:30",
    "id": 2,
    "instructor": "Jane",
    "max_slots": 10,
    "name": "Zumba"
    },
    {
    "available_slots": 2,
    "date": "05-07-2025 07:00",
    "id": 4,
    "instructor": "Sam",
    "max_slots": 10,
    "name": "Yoga"
    }
    ]

    ii) if not:
    {'message': 'No upcoming classes found'}

5.  "/api/book?tz=TimeZone": "Book a class required fields[class_id,client_name,client_email]" [POST]

    -example payload:

            {
              "class_id":3,
              "client_name": "tony",
              "client_email": "tony@example.com"
            }



    -expected o/p:
    -if booking successful:
    {
    "class": {
    "available_slots": 3,
    "date": "2025-03-11 05:30:00 IST",
    "id": 3,
    "instructor": "Tony",
    "max_slots": 20,
    "name": "HIIT"
    },
    " message": "Booking successful"
    }

             -if slot not available:
                     {'error': 'No available slots for this class'}

             -if duplicate bookings:
                     {'error': 'You have already booked this class'}

             -if class not found:
                     {'error': 'Class not found'}

             -if missing field:
                     {'error': 'Missing required fields'}



=================================Thank you==============================================