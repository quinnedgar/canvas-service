
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time
import redis
import os
import signal
import threading

r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["chrome-extension://*"]) #change * to real id later


@app.route('/import_url', methods=['POST', 'OPTIONS'])
def handle_import(): 
    if request.method == 'OPTIONS':
        return '', 200
    else:
        global Url
        Url = request.get_json().get('url')
        r.publish('URL Comm', Url)
        time.sleep(1)
        return jsonify({"status": "success", "recieved": Url})
    
@app.route('/shutdown', methods=['POST'])
def shutdown():
    def shutdown_app():
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGINT)


    threading.Thread(target=shutdown_app, daemon=True).start()
    
    return 'Server shutting down...', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






