from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse  
import re

app = Flask(__name__)
api = Api(app, prefix='/api')  
parser = reqparse.RequestParser()
parser.add_argument('path', type=str, action="append") 


class DefangResource(Resource):

	def get(self):   
		args = parser.parse_args()
		paths = args['path']

		defanged = []
		for path in paths:
			defanged.append(defang(path))

		return jsonify({"defanged": defanged})
 
 
class RefangResource(Resource): 

	def get(self):  
		args = parser.parse_args()
		paths = args['path']

		refanged = []
		for path in paths:
			refanged.append(refang(path))

		return jsonify({"refanged": refanged})

def defang(path): 
	path = path.replace(".",  "[dot]")
	path = path.replace("/",  "\/")
	path = path.replace("http",  "hxxp") 
	return path 

def refang(path): 
	path = path.replace("[dot]", ".")
	path = path.replace("\/", "/")
	path = path.replace("hxxp",  "http") 
	return path 

 

if __name__ == '__main__': 
	api.add_resource(DefangResource, '/defang')
	api.add_resource(RefangResource, '/refang')

	app.run(debug=True) 
 
	# Defang: 
	# 	Example curl request 
	# 	curl -X GET 'http://127.0.0.1:5000/api/defang?path=https://twitter.com'

	# 	Example with multiple paths
	# 	curl -X GET 'http://127.0.0.1:5000/api/defang?path=https://twitter.com&path=https://google.com'

	# Refang: 
	# 	Example curl request 
	# 	curl -X GET 'http://127.0.0.1:5000/api/refang?path=hxxps:\/\/twitter[dot]com'

	# 	Example with multiple paths
	# 	curl -X GET 'http://127.0.0.1:5000/api/refang?path=hxxps:\/\/twitter[dot]com&path=hxxps:\/\/google[dot]com'

