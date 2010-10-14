import sqlite3 as sqlite

connection = sqlite.connect('rundb.db')
#memoryConnection = sqlite.connect(':memory:')

cursor = connection.cursor()
cursor.execute("CREATE TABLE RUNSTATUS ( \
				id INTEGER PRIMARY KEY,  \
				run VARCHAR(10),  \
				listener VARCHAR(50), \
				status VARCHAR(20), \
				validated VARCHAR(20), \
				rawpath VARCHAR(100), \
				nfiles VARCHAR(100), \
				rawstatus VARCHAR(20) \
				)")
connection.commit()

cursor.execute("CREATE TABLE RUNPARAMS ( \
				id INTEGER PRIMARY KEY,  \
				run VARCHAR(10),  \
				start VARCHAR(20), \
				runtype VARCHAR(20), \
				daqconfig VARCHAR(20), \
				detmask INTEGER, \
				filetag VARCHAR(50), \
				rec VARCHAR(20), \
				datasource VARCHAR(20), \
				stop VARCHAR(20), \
				totaltime VARCHAR(20), \
				cleanstop VARCHAR(20), \
				maxlb VARCHAR(20), \
				partname VARCHAR(50), \
				recevents VARCHAR(50), \
				storedevents VARCHAR(50), \
				l1events VARCHAR(50), \
				l2events VARCHAR(50), \
				efevents VARCHAR(50), \
				errcode VARCHAR(50), \
                                tierzerotag VARCHAR(50) \
				)")

connection.commit()


cursor.execute("CREATE TABLE JOBSTATUS ( \
				id INTEGER PRIMARY KEY,  \
				run VARCHAR(10),  \
				jobconfiguration VARCHAR(50), \
				batchid VARCHAR(20), \
				status VARCHAR(20), \
				result VARCHAR(20), \
				validation VARCHAR(20), \
				rawpath VARCHAR(100), \
				jobstart VARCHAR(30), \
				jobend VARCHAR(30) \
				)")
connection.commit()

cursor.close()
connection.close()
