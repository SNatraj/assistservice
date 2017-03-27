#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import make_response


# Flask app should start in global layout
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = CLEARDB_DATABASE_URL
#db = SQLAlchemy(app)

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
	
	print("Response:")
    print(speech)
	
	#query = "INSERT INTO  (action, cuisine_type,distance) VALUES(:action-data,:cuisine-type-data,:restaurant-distance-data)"
	#data = {
	#				'action-data': req.get("result").get("action"),
	#				'cuisine-type-data': parameters.get("cuisine-type"),
	#				'restaurant-distance-data': parameters.get("restaurant-distance"),
	#	   }
    #mysql.query_db(query, data)
	


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
