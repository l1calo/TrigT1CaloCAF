import sqlite3 as sqlite

connection = sqlite.connect('rundb.db')
#memoryConnection = sqlite.connect(':memory:')

cursor = connection.cursor()

cursor.execute("select run, partname, tierzerotag from RUNPARAMS")

for row in cursor:
    print str(row[0]), str(row[1]), str(row[2])

cursor.close()
connection.close()
