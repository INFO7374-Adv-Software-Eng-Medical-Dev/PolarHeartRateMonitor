import sqlite3


# test database

# path = 'data/patients.db'
path ="data/data_buffer.db"

conn = sqlite3.connect(path)

c = conn.cursor()
# c.execute('''INSERT INTO patients (name, age, height, weight) VALUES (?, ?, ?, ?)''', ('John Doe', 30, 180, 70))
# # Commit the changes
# conn.commit()
# #Query all the patients
result = c.execute('''SELECT * FROM data''')
patients = result.fetchall()

print(patients)

# Insert the patient's data into the database

