#!/usr/bin/env python

__doc__ = """
ResetJob.py

Usage: python ResetJob.py RUNNUMBER JOBTYPE

e.g.: python ResetJob.py 144830 Phos4ShapeMaker
"""

import os, sys, traceback
import sqlite3

def startJob(run, type):
    """ updates the database to reset the job. """
    id = queryId(run, type)
    print id
    cursor.execute("update jobstatus set validation='YES' where id = ?", (id,))
    cursor.fetchone()

def queryId(run, type):
    """ queries the database for the id of the job. """
    cursor.execute("select id from jobstatus where run = ? and jobconfiguration = ?", (run, type))
    return cursor.fetchone()[0]

if __name__ == "__main__":
    global cursor
    try:
        conn = sqlite3.connect(os.path.join(os.path.dirname(sys.argv[0]), "db", "rundb.db")) #hardcoded for now
        cursor = conn.cursor()
        startJob(sys.argv[1], sys.argv[2])
        conn.commit()
        print "Successfully started job (%s, %s)!" % (sys.argv[1], sys.argv[2])
    except:
        traceback.print_exc()

    if conn: conn.close()
