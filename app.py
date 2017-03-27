#!/usr/bin/env python

import urllib
import json
import os import environ
import MySQLdb
import urlparse


from flask import Flask, flash, url_for, redirect, render_template, jsonify
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
urlparse.uses_netloc.append('mysql')

try:

    # Check to make sure DATABASES is set in settings.py file.
    # If not default to {}

    if 'DATABASES' not in locals():
        DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})

        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })
		
except Exception:
    print 'Unexpected error:', sys.exc_info()

db = MySQLdb.connect(HOST, USER, PASSWORD, NAME)
cursor = db.cursor()


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

	query = "INSERT INTO  (action, cuisine_type,distance) VALUES(:action-data,:cuisine-type-data,:restaurant-distance-data)"
	data = {
					'action-data': req.get("result").get("action"),
					'cuisine-type-data': parameters.get("cuisine-type"),
					'restaurant-distance-data': parameters.get("restaurant-distance"),
		   }
    
	cursor.execute(query,data)
	db.commit()
 

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
