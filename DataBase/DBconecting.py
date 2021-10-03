import mysql.connector

my_db = mysql.connector.connect(
  host="localhost",
  user="youngster",
  password="nopassword"
)

my_cursor = my_db.cursor()

my_cursor.execute("SHOW DATABASES")

for x in my_cursor:
  print(x)