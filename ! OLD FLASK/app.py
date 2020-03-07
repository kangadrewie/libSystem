from flask import Flask, render_template, request, jsonify
import sys
import json
from libsys import *

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

# @app.route('/getIP', methods=['POST', 'GET'])
# def background_process_test():

# 	jobTitle = request.form['jobTitle']
# 	location = request.form['location']

# 	if jobTitle and location:
# 		js = JobSearch(jobTitle, location)
# 		s = js.soup()
# 		jsonCloud = js.wordCloud()
		
# 		return jsonify({'wordcloud' : jsonCloud, 'title' : jobTitle, 'loc' : location})


if __name__ == '__main__':
	app.run(debug=True)