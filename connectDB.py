import cx_Oracle
# Make connection to Oracle and handle exception;

con = None
cursor = None

def connect_db():
	global con
	global cursor
	try:
		con = cx_Oracle.connect("system/abc123")
		print("Connected")
		cursor = con.cursor()

	except cx_Oracle.DatabaseError as e:
		print("ISSUE "+e)

def disconn_db():
	if cursor is not None:
		cursor.close()
	if con is not None:
		con.close()
		print("Disconnected")