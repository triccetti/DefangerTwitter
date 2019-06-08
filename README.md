# DefangerTwitter
### Author: Taylor Riccetti
An api that *defangs* and *refangs* url paths. 

#### Example usage with requests  
> response = requests.post(url="http://127.0.0.1:5000/api/defang", json= {"path" : "https://twitter.com"}) 
> response = requests.post(url="http://127.0.0.1:5000/api/refang", json= {"path" : "hxxps:\\/\\/twitter[dot]com"})
> response = requests.post(url="http://127.0.0.1:5000/api/refang", json= {"path" : "hxxps:\\/\\/twitter[dot]com", "encode" : true})

#### Example usage with curl
>  $ curl -X POST "http://127.0.0.1:5000/api/defang?path=https://twitter.com"

>  $ curl -X POST "http://127.0.0.1:5000/api/refang?path=hxxps:\/\/twitter[dot]com"

>  $ curl -X POST "http://127.0.0.1:5000/api/refang?path=hxxps:\/\/twitter[dot]com&encode=True"

#### Response: 
> "defang_response": [ "hxxps:\\/\\/twitter[dot]com" ]
> "refang_response": [ "https://twitter.com" ]
> "refang_response": [ "https%3A%2F%2Ftwitter.com" ] 
