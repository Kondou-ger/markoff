#coding: utf-8
from flask import Flask, render_template, redirect, request, url_for, jsonify
from time import sleep
from random import random
import markoff

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/chat/')
def chat():
	connection = markoff.markoff("markoff.db")
	sleep(random()+random())
	try:
		connection.add(request.args['text'])
	except UnicodeEncodeError:
		answer = "I don't understand Unicode :(" # Or do I?
		return jsonify(text=answer)

	try:
		answer = connection.create()
	except:
		answer = ""

	return jsonify(text=answer)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
