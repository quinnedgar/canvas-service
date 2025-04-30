from flask import Flask, request, jsonify
import requests
import json
import socket
import subprocess
import time
import os, signal, threading

######## NOTE: Windows: Install ollama on PATH or subprocess will fail
### Windows winget search ollama, winget install Ollama.Ollama

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if not check_port(11434):
    ollama_process = subprocess.Popen(
    ['ollama', 'serve'], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    )
    print(f'Starting Ollama on PID: {ollama_process.pid}')


app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate" #http://10.0.0.30:5000/api/endpoint
OLLAMA_MODEL = "gemma3" 

prompt_direction = 'Respond exclusively with the answer in a JSON object form'


@app.route('/receive', methods=['POST'])
def recieve():
    body = request.json
    question = body['question']
    choices = body['choices']
    

    question_obj = {
        "question": question,
        "answer_choices": choices
    }

    prompt = f"{json.dumps(question_obj)}, {prompt_direction}"
    global response

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
            #"format": "json"
        })
    
    except Exception as e:
        print(f"\n Exception: {e}\n")

    if response.status_code != 200: 
        return jsonify({"error": "Ollama API Query Fail"}), 500

    model_result = response.json().get('response', '').strip()
  
    for c in choices:
        if c in model_result:
            return c
        else:
            return jsonify({
            "response": model_result
            })

    
@app.route('/shutdown', methods=['POST'])
def shutdown():
    def shutdown_app():
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGINT)

    threading.Thread(target=shutdown_app, daemon=True).start()
    
    return 'Server shutting down...', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
