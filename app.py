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



cnx = mysql.connector.connect(user='root', password='Natraj123$',
                              host='localhost',
                              database='assistservice')
cursor=cnx.cursor()
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
    cuisine_type = parameters.get("cuisine_type")

    speech = "Cuisine is" + cuisine_type

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')



add_employee = ("INSERT INTO employee "
               "(first_name, last_name, gender) "
               "VALUES (%s, %s, %s)")

data_employee = (cuisine_type, 'Vanderkelen', 'M')

# Insert new employee
cursor.execute(add_employee, data_employee)


# Make sure data is committed to the database
cnx.commit()
query = ("SELECT first_name, last_name FROM employee ")
        


cursor.execute(query)

for (first_name, last_name) in cursor:
  print("{}, {} was hired on".format(
    last_name, first_name))
cursor.close()
cnx.close()