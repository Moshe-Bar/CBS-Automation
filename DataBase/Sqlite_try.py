import sqlite3

conn = sqlite3.connect('Data.db')

c = conn.cursor()

# c.execute("""CREATE TABLE employees (
#             first text,
#             last text,
#             pay integer
#             )""")

# c.execute("INSERT INTO employees VALUES ('Corey','Schafer', 50000)")
#
# c.execute("SELECT * FROM employees WHERE last='Schafer'")
conn.commit()
conn.close()