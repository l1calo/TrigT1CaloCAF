import sqlite3 as sqlite

connection = sqlite.connect('rundb.db')
#memoryConnection = sqlite.connect(':memory:')

cursor = connection.cursor()
cursor.execute("ALTER TABLE RUNPARAMS ADD COLUMN tierzerotag VARCHAR(50)")

connection.commit()

cursor.close()
connection.close()
