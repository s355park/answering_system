from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin requests
from api import get_ans

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()  # Get the JSON data from the request
    query = data.get('query', '')

    # Process the query and generate a response
    # For this example, let's just echo the query
    answer = get_ans(query)
    print(answer)

    # Return the response in JSON format
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
