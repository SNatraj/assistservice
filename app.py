#!/usr/bin/env python

import urllib
import json
import os
import mysql.connector


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
	
	makeinsert(req)
		
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
	
def makeinsert(req):
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
	return {}
	
def makeWebhookResult(req):
    if req.get("result").get("action") != "food.discovery":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    cuisine = parameters.get("cuisine-type")

 

    speech = "Cuisine is " + cuisine

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-assistservice1"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
