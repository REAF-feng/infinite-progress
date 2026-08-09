#!/usr/bin/env python3
"""
Launch script for the Medical Diagnosis Assistant Flask application
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set environment variables if not already set
if not os.getenv('FLASK_APP'):
    os.environ['FLASK_APP'] = 'app_flask.py'

if not os.getenv('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'development'

# Import and run the Flask app
try:
    from app_flask import app
    
    print("=" * 60)
    print("🏥 Medical Diagnosis Assistant - Flask Application")
    print("=" * 60)
    print("📊 AI-Powered Differential Diagnosis Tool")
    print("⚠️  For Educational Purposes Only")
    print("=" * 60)
    print("🌐 Starting Flask development server...")
    print("🔗 Access the application at: http://localhost:5000")
    print("=" * 60)
    
    # Run the application
    if __name__ == '__main__':
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=bool(os.environ.get('DEBUG', True))
        )
        
except ImportError as e:
    print(f"❌ Error importing Flask application: {e}")
    print("💡 Make sure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)
