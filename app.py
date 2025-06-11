
from flask import Flask, request, jsonify
import os
from retriever import retrieve_similar
from generate_response import generate_response

app = Flask(__name__)

# Define your secret token (in production, store this securely)
VALID_TOKEN = "mysecrettoken123"
print("Starting Flask app...")


@app.route('/', methods=['GET'])
def hello():
    return "Hi"

@app.route('/api/search', methods=['POST'])
def search():
    try:
        # Check Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token is missing or invalid'}), 401

        token = auth_header.split(' ')[1]
        if token != VALID_TOKEN:
            return jsonify({'error': 'Invalid token'}), 403

        # Get query from JSON payload
        data = request.get_json()
        query = data.get('query')
        top_k = data.get('top_k', 3)

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        results = retrieve_similar(query, top_k=top_k)
        results = generate_response(query, results)

        return jsonify({
            'query': query,
            'results': results.split('\n\n') if results else [],
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
