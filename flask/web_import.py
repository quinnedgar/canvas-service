
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, supports_credentials=True, origins=["chrome-extension://*"]) #change * to real id later
@app.route('/import_url', methods=['POST', 'OPTIONS'])

def handle_import():
    if request.method == 'OPTIONS':
        return '', 200
    else:
        Url = request.get_json().get('url')
        print(f'Recieved: {Url}')
        return jsonify({"status": "success", "recieved": Url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
