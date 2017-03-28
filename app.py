#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import make_response
from config import config

import json
import os 

cursor = conn.cursor()

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
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "food.discovery":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    cuisine = parameters.get("cuisine-type")

	#query = "INSERT INTO  EntitySessionTestTbl (action, cuisine_type,distance) VALUES(:action-data,:cuisine-type-data,:restaurant-distance-data)"

	#data = {
	#		'action-data': req.get("result").get("action"),
	#		'cuisine-type-data': parameters.get("cuisine-type"),
	#		'restaurant-distance-data': parameters.get("restaurant-distance"),
	#		}
    
	#cursor.execute(query,data)
	#conn.commit()
	#cursor.close()
	#conn.close()

    speech = "Cuisine is " + parameters.get("cuisine-type") + " " + parameters.get("restaurant-distance")
	
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
