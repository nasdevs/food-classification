from app import app
from flask import jsonify

@app.route('/')
def index():
    return jsonify({
        'status': {
            'code': 200,
            'message': 'Success fetching the API'
        },
        'data': None
    }), 200