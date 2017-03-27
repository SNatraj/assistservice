#!/usr/bin/env python

#import urllib
import json
import os 
#import MySQLdb
#import urlparse
import mysql.connector

from flask import Flask, flash, url_for, redirect, render_template, jsonify, request, make_response
#from flask.ext.sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import text

# Flask app should start in global layout
app = Flask(__name__)
#app.config.setdefault('SQLALCHEMY_DATABASE_URI', environ.get('DATABASE_URL'))
#app.config['SQLALCHEMY_DATABASE_URI'] = CLEARDB_DATABASE_URL
#db = SQLAlchemy(app)

db = mysql.connector.connect(
   'driver'    => 'mysql',
   'host'      => env('DB_HOST', 'us-cdbr-iron-east-03.cleardb.net'),
    'database'  => env('DB_DATABASE', 'heroku_07453e514633ec3'),
   'username'  => env('DB_USERNAME', 'b4d6e46002fc68'),
    'password'  => env('DB_PASSWORD', '55fbc72d'),
    'charset'   => 'utf8',
    'collation' => 'utf8_unicode_ci',
    'prefix'    => '',
    'strict'    => false)

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

#	query = "INSERT INTO  (action, cuisine_type,distance) VALUES(:action-data,:cuisine-type-data,:restaurant-distance-data)"
#	data = {
#				'action-data': req.get("result").get("action"),
#				'cuisine-type-data': parameters.get("cuisine-type"),
				
#				'restaurant-distance-data': parameters.get("restaurant-distance"),
#		   }
    
#	cursor.execute(query,data)
#	db.commit()
 

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
