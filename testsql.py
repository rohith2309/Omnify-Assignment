import sqlite3

conn=sqlite3.connect('instance/fitness.db')
c = conn.cursor()

c.execute("SELECT * FROM fitness_class")
classes = c.fetchall()
print("============================================================")
print("Classes:")
for cls in classes:
    print(cls)


c.execute("SELECT * FROM booking")
bookings = c.fetchall() 
print("============================================================")
print("\n Bookings:")

for booking in bookings:
    print(booking)