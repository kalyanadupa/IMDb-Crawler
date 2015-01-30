

import MySQLdb

db = MySQLdb.connect("10.5.18.67","12CS30001","dual12","12CS30001")

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql = "SELECT * FROM Investigator"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      
      # Now print fetched result
      print "Code =%s,EC =%s" % \
             (fname, lname )
except:
   print "Error: unable to fecth data"

# disconnect from server
db.close()


