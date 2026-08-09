from flask import Flask, render_template, request, jsonify
from engine_flask import RAG_Engine
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize the RAG engine
try:
    rag_engine = RAG_Engine()
    logger.info("RAG Engine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG Engine: {e}")
    rag_engine = None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@app.route('/diseases')
def diseases():
    """Render the diseases information page"""
    # Get list of available diseases from data directory
    data_path = "./data"
    diseases_list = []
    
    if os.path.exists(data_path):
        for filename in os.listdir(data_path):
            if filename.endswith(".txt"):
                disease_name = filename.replace(".txt", "").replace("_", " ").title()
                diseases_list.append(disease_name)
    
    return render_template('diseases.html', diseases=diseases_list)

@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    """Analyze patient symptoms using RAG engine"""
    try:
        if not rag_engine:
            return jsonify({
                'success': False,
                'error': 'AI engine not available. Please try again later.'
            })
        
        data = request.get_json()
        symptoms = data.get('symptoms', '').strip()
        
        if not symptoms:
            return jsonify({
                'success': False,
                'error': 'Please enter symptoms before analyzing.'
            })
        
        # Get analysis from RAG engine
        analysis_result = rag_engine.query(symptoms)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'symptoms': symptoms
        })
        
    except Exception as e:
        logger.error(f"Error analyzing symptoms: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while analyzing symptoms. Please try again.'
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'rag_engine_status': 'available' if rag_engine else 'unavailable'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
