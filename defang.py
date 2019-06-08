from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse   
from urllib.parse import quote_plus, unquote_plus

# Create api
app = Flask(__name__)
api = Api(app, prefix="/api")  

# Parameters to be parsed for
parser = reqparse.RequestParser()
parser.add_argument("path", type=str, required=True, action="append") 
parser.add_argument("encode", type=bool, required=False) 
  
'''
	/api/defang endpoint
	
	Params: path: a list of all paths to defang 
	Returns: Json list of defanged paths 
'''
class DefangResource(Resource): 
	def post(self):   
		args = parser.parse_args(strict=True) 
		paths = args["path"]

		defanged = []
		for path in paths:
			defanged.append(defang(path)) 

		return {"defang_response": defanged}, 200
 

'''
	/api/refang endpoint 
	
	Params: path: a list of all paths to refang
			encode: (optional) encodes the refanged paths
	Returns: Json list of refanged paths 
'''
class RefangResource(Resource):  
	def post(self):  
		args = parser.parse_args(strict=True)  
		paths = args["path"]
		encode = args["encode"]

		refanged = []
		for path in paths:
			refanged_path = refang(path)
			if(encode):
				refanged_path = quote_plus(refanged_path)
			refanged.append(refanged_path)

		return {"refang_response": refanged}, 200 


#	Defang the given path
def defang(path): 
	new_path = path

	if(is_encoded(path)): 
		new_path = unquote_plus(path) 

	new_path = new_path.replace(".",  "[dot]")
	new_path = new_path.replace("/",  "\\/")  
	new_path = new_path.replace("http", "hxxp") 

	return new_path

 
# Refang the given path
def refang(path): 
	new_path = path
 
	new_path = new_path.replace("[dot]", ".")
	new_path = new_path.replace("\\/", "/") 
	new_path = new_path.replace("hxxp", "http") 

	return new_path


# Checks if the given path has been encoded
def is_encoded(path): 
	decoded = unquote_plus(path)
	encoded = quote_plus(decoded)  
	return (encoded == path)

if __name__ == "__main__": 
	api.add_resource(DefangResource, '/defang')
	api.add_resource(RefangResource, '/refang')

	app.run(debug=True)  

	# example usage with requests
	#	requests.post(url=defang_url, json= {"path" : "https://twitter.com"})

	# example usage with curl
	#	curl -X POST "http://127.0.0.1:5000/api/defang?path=https://twitter.com"