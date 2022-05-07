from flask import Flask, json, request

api = Flask(__name__)
host, port = ("127.0.0.1", 8080)

@api.route('/', methods=['GET'])
def index():
    return json.dumps("server up")

@api.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    print("data =", data)
    print("request.data", request)
    return json.dumps("log recived")

if __name__ == '__main__':
    api.run(host=host, port=8080)