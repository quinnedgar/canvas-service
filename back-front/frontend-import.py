
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, supports_credentials=True, origins="chrome-extension://*")


@app.route('/import_url', methods=['POST', 'OPTIONS'])
@cross_origin(origins='chrome-extension://*')
def handle_import():
    if request.method == 'OPTIONS':
        return '', 200
    else:
        Url = request.get_json().get('url')
        print(f'Recieved: {Url}')
        return jsonify({"status": "success", "received_url": Url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
