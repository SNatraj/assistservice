#!/usr/bin/env python

import urllib
import json
import os

import mysql.connector
from mysql.connector import errorcode
try:
  cnx = mysql.connector.connect(host = "localhost",
                       user = "root",
                       passwd = "Natraj123$",
                       db = "assistservice")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
  
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
cnx = mysql.connector.connect(host = "localhost",
                       user = "root",
                       passwd = "Natraj123$",
                       db = "assistservice")

cursor =cnx.cursor()


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "food.discovery":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    cuisine = parameters.get("cuisine-type")

    speech = "Cuisine is " + parameters.get("cuisine-type") + " " + parameters.get("restaurant-distance")
	add_employee = ("INSERT INTO employees "
               "(first_name, last_name,  gender) "
               "VALUES (%s, %s, %s,)")

	data_employee = (parameters.get("cuisine-type"), parameters.get("restaurant-distance"),  'M')

	cursor.execute(add_employee, data_employee)

	cnx.commit()

	cursor.close()
	cnx.close()
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
