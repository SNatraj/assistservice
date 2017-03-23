#!/usr/bin/env python

import mysql.connector


	cnx = mysql.connector.connect(user='root', password='Natraj123$',
                              host='localhost',
                              database='assistservice')
	cursor=cnx.cursor()
	
	add_employee = ("INSERT INTO employees "
               "(first_name,last_name,gender) "
               "VALUES (%s,%s, %s,)")


	data_employee = ('Abc', 'ABC','M')

	# Insert new employee
	cursor.execute(add_employee, data_employee)

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()

	

