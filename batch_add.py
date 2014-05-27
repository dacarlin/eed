import sqlite3
from sys import argv

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

with open(argv[1], 'r') as batch:
  for line in batch:
    entry = r"('" + r"', '".join(line.strip().split(", ")) + r"')"
    print(entry)
    cursor.execute("INSERT INTO enter_entry VALUES " + entry)
    connection.commit()

connection.close()
