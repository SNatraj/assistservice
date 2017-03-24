#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flaskext.mysql import MySQL
from flask import request
from flask import make_response
mysql = MySQL()
# Flask app should start in global layout
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Natraj123$'
app.config['MYSQL_DATABASE_DB'] = 'assistservice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


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
	
	#add_employee = ("INSERT INTO employee "
     #          "(first_name, last_name,  gender) "
      #         "VALUES (%s, %s, %s,)")

	#data_employee = (parameters.get("cuisine-type"), parameters.get("restaurant-distance"),  'M')
	#cursor = mysql.connect().cursor()
	#cursor.execute(add_employee, data_employee)

	#connection.commit()

	#cursor.close()
	#connection.close()
	
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
