from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
import socket
from werkzeug.middleware.proxy_fix import ProxyFix
import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure CORS to allow all origins
CORS(app, 
     resources={r"/*": {
         "origins": "*",
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": "*",
         "expose_headers": "*",
         "supports_credentials": False,
         "max_age": 3600
     }},
     supports_credentials=False)

@app.after_request
def after_request(response):
    # Add CORS headers
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'false')
    response.headers.add('Access-Control-Max-Age', '3600')
    response.headers.add('Access-Control-Expose-Headers', '*')
    return response

@app.route('/', methods=['GET'])
def home():
    try:
        # Get server information
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        return jsonify({
            'status': 'running',
            'message': 'PDF Chat Backend Server is running',
            'server_info': {
                'hostname': hostname,
                'ip_address': ip_address,
                'port': 5000
            },
            'endpoints': {
                '/': 'GET - Server information',
                '/health': 'GET - Health check',
                '/chat': 'POST - Send chat messages'
            }
        })
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error getting server information: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Get server information
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        return jsonify({
            'status': 'healthy',
            'message': 'Server is healthy',
            'server_info': {
                'hostname': hostname,
                'ip_address': ip_address,
                'port': 5000
            }
        })
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'message': f'Error checking server health: {str(e)}'
        }), 500

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
        
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            logger.error("No message provided in request")
            return jsonify({'error': 'No message provided'}), 400
        
        # Here you can implement your chat logic
        # For now, we'll just echo back the message
        try:
            # Get relevant document chunks
            results = main.search_stored_documents(data['message'])
            
            # Generate response using Gemini
            prompt = f"""
            You are a helpful assistant that can answer questions about the documents in the following list.
            Please format your response with proper paragraphs, bullet points, and numbered lists where appropriate.
            Make sure to use markdown formatting for better readability.
            
            Documents:
            {results}
            
            Question: {data['message']}
            """
            response = main.model.generate_content(prompt)
            reply = response.text.strip()
            
            # Create chat message object
            chat_message = {
                'query': data['message'],
                'response': reply
            }
            
            return jsonify(chat_message)
    
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            response = f"Received your message: {data['message']}"

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested URL was not found on the server.',
        'available_endpoints': ['/', '/health', '/chat']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred.'
    }), 500

if __name__ == '__main__':
    try:
        # Get server information
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        logger.info(f"Starting PDF Chat Backend Server...")
        logger.info(f"Server running on: {ip_address}:5000")
        logger.info(f"Hostname: {hostname}")
        
        # Run the Flask app with optimized settings
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Disable debug mode in production
            threaded=True,  # Enable threading
            use_reloader=False  # Disable reloader
        )
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise 