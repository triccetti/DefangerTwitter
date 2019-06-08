import requests
from flask import jsonify
import unittest

defang_url = "http://127.0.0.1:5000/api/defang"
refang_url = "http://127.0.0.1:5000/api/refang"

'''
	Test the defang endpoint from defang.py
'''
class TestDefang(unittest.TestCase):
	
	def test_defang_path(self):
		defang_response = requests.post(url=defang_url, json= {"path" : "https://twitter.com"}).json() 
		result = defang_response["defang_response"][0]
		self.assertEqual(result, "hxxps:\\/\\/twitter[dot]com")

	def test_defang_multiple(self):
		expected = ["hxxps:\\/\\/twitter[dot]com",
					"hxxps:\\/\\/twitter[dot]com\\/hello world",  
					"hxxps:\\/\\/lmgtfy[dot]com\\/?q=hello world",
					"example[dot]domain[dot]com",
					"8[dot]8[dot]8[dot]8"]

		defang_response = requests.post(url=defang_url,
										json={"path" : ["https://twitter.com",
														"https://twitter.com/hello world",  
														"https://lmgtfy.com/?q=hello world",
														"example.domain.com",
														"8.8.8.8"]}).json() 
		result = defang_response["defang_response"]
		self.assertEqual(result, expected) 

	def test_no_paths(self):
		result = requests.post(url=defang_url).json() 
		self.assertEqual(result, {"message": {"path":
			"Missing required parameter in the JSON body or the post body or the query string"}}) 

	def test_encoded_defang_path(self):
		defang_response = requests.post(url=defang_url, json= {"path" : "https%3A%2F%2Ftwitter.com"}).json()
		result = defang_response["defang_response"][0] 
		self.assertEqual(result, "hxxps:\\/\\/twitter[dot]com") 

'''
	Test the defang endpoint from defang.py
'''
class TestRefang(unittest.TestCase):
	
	def test_refang_path(self):
		refang_response = requests.post(url=refang_url, json= {"path" :"hxxps:\\/\\/twitter[dot]com"}).json()
		result = refang_response["refang_response"][0]
		self.assertEqual(result, "https://twitter.com") 


	def test_refang_path_encoded(self):
		refang_response = requests.post(url=refang_url, json= {"path" :"hxxps:\\/\\/twitter[dot]com",
															   "encode" : True}).json()
		result = refang_response["refang_response"][0]
		self.assertEqual(result, "https%3A%2F%2Ftwitter.com") 


	def test_refang_multiple(self):
		expected = ["https://twitter.com",
					"https://twitter.com/hello world",
					"https://lmgtfy.com/?q=hello world", 
					"example.domain.com",
					"8.8.8.8"]

		refang_response = requests.post(url=refang_url,
										json= {"path" : ["hxxps:\\/\\/twitter[dot]com",
														 "hxxps:\\/\\/twitter[dot]com\\/hello world", 
														 "https://lmgtfy.com/?q=hello world", 
														 "example[dot]domain[dot]com",
														 "8[dot]8[dot]8[dot]8"]}).json() 	
		result = refang_response["refang_response"]
		self.assertEqual(result, expected) 


	def test_refang_multiple_encoded(self):
		expected = ["https%3A%2F%2Ftwitter.com",
					"https%3A%2F%2Ftwitter.com%2Fhello+world",
					"https%3A%2F%2Flmgtfy.com%2F%3Fq%3Dhello+world",
					"example.domain.com", 
					"8.8.8.8"]

		refang_response = requests.post(url=refang_url,
										json= {"path" : ["hxxps:\\/\\/twitter[dot]com",
														 "hxxps:\\/\\/twitter[dot]com\\/hello world", 
														 "https://lmgtfy.com/?q=hello world", 
														 "example[dot]domain[dot]com",
														 "8[dot]8[dot]8[dot]8"],
												"encode" : True}).json() 
		result = refang_response["refang_response"]
		self.assertEqual(result, expected) 

	def test_no_paths(self):
		result = requests.post(url=refang_url).json() 
		self.assertEqual(result, {"message": {"path": 
			"Missing required parameter in the JSON body or the post body or the query string"}}) 


if __name__ == '__main__':
	unittest.main()

 