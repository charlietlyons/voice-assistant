from flask import Flask, jsonify
import json
import urllib.request

app = Flask(__name__)

@app.route('/')
def startServer():
    data = json.dumps({
        "model": "gpt-3.5-turbo-16k-0613",
        "messages": [{"role": "user", "content": "Say this is a test, but like you really don't like me and which I would stop bothering you."}],
        "temperature": 0.7
    }).encode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer someToken'
    }
    
    req = urllib.request.Request('https://api.openai.com/v1/chat/completions', data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            headers = response.getheaders()
            print(headers)
            response_data = json.loads(response.read().decode('utf-8'))
            return jsonify(response_data)
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP Error: {e.code} - {e.reason}"}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
