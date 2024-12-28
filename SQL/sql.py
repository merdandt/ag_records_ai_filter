import sqlite3
import ddl as ddl
import dml as dml

## Connect to database
conn = sqlite3.connect('ag_records.db')

## Create a cursor
cursor = conn.cursor()

## Create a table
cursor.execute(ddl.AGRECORD_DDL)

## Insert data into table
# Split the string text to new line and execute one by one
for line in dml.INSERT_DML.split("\n"):
    cursor.execute(line)

## Diisplay the inserted data
print("Inserted data are: ")
data = cursor.execute("SELECT * FROM AgRecords")

for row in data:
    print(row) 

## Close the connection
conn.commit()
conn.close()