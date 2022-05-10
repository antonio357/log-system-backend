from flask import Flask, json, request, make_response
import requests
from time import sleep

api = Flask(__name__)
host, port = ("0.0.0.0", 8080)

@api.route('/', methods=['GET'])
def index():
    return json.dumps("server up")

@api.route('/log', methods=['POST'])
def log():
    data = request.get_data()
    print("data =", data)
    print("request", request)
    response = make_response("this is a response from python server", 200)
    response.mimetype = "text/plain"
    return response

# while (True):
#     # sleep(1000)
#     print("making get request")
#     print(requests.patch("http://192.168.4.1/start").content)

if __name__ == '__main__':
    api.run(host=host, port=8080)
    # while (True):
    #     # sleep(1000)
    #     print("making get request")
    #     print(requests.get("http://192.168.4.1/").content)
