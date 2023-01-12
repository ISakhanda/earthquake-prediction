import requests
import json
import time
import os
import socket



#URL to add rules for tweet search

endpoint_rules = "https://api.twitter.com/2/tweets/search/stream/rules"


#Body to add into Post request (so this is not "parameter" but "json" part in your Post request)
query_parameters = {
"add": [
    {"value":"earthquake lang:en "}
]
}

#Your bearer token to access Twitter streaming API
bearer_token = os.getenv("bearer_token")


def request_headers(bearer_token: str) -> dict:
    """
    Sets up the request headers. 
    Returns a dictionary summarising the bearer token authentication details.
    """
    return {"Authorization": "Bearer {}".format(bearer_token)}


headers = request_headers(bearer_token)


def connect_to_endpoint(endpoint_url: str, headers: dict, parameters: dict) -> json:
    """
    Connects to the endpoint and post customized filter for tweet search.
    Returns a json with data to show if your custom filter rule is created.
    
    """
    response = requests.request(
        "POST", url=endpoint_url, headers=headers, json=parameters
    )
    
    return response.json()



endpoint_get = "https://api.twitter.com/2/tweets/search/stream"



def get_tweets(url,headers):
    """
    Fetch real-time tweets based on your custom filter rule.
    Returns a Json format data where you can find Tweet id, text and some metadata.
    Sends the data to your defined local port where Spark reads streaming data.
    """
    get_response = requests.get(url=url,headers=headers,stream=True)


    if get_response.status_code!=200:
        print(get_response.status_code)
    
    else:
        for line in get_response.iter_lines():
            if line==b'':
                pass
            else:
                json_response = json.loads(line)  #json.loads----->Deserialize fp (a .read()-supporting text file or binary file containing a JSON document) to a Python object using this conversion table.ie json to python object 
                conn.send(bytes(str(json_response["data"]) + "\n",'utf-8'))




if __name__ == "__main__":

    # Set localhost socket parameters
    localhost = "127.0.0.1"
    local_port = 9095

    # Create local socket
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind((localhost, local_port))
    local_socket.listen(1)

    conn, addr = local_socket.accept()
    print("Connected by", addr)

    json_response = connect_to_endpoint(endpoint_rules, headers, query_parameters)
    print(json_response)

    get_tweets(endpoint_get,headers)





