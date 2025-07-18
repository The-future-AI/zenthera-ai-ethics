from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os

# Import route modules
from routes.compliance import compliance_bp
from routes.regulation import regulation_bp

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='static')
    
    # Enable CORS for all routes
    CORS(app, origins="*")
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'zenthera-dev-key-2025')
    app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///zenthera.db')
    
    # Register blueprints
    app.register_blueprint(compliance_bp, url_prefix='/api/compliance')
    app.register_blueprint(regulation_bp, url_prefix='/api/regulation')
    
    @app.route('/')
    def index():
        """Main dashboard route"""
        return render_template('index.html')
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "ZenThera AI Ethics Platform",
            "version": "1.0.0",
            "features": [
                "ZenThera Compliance Grid (ZCG)",
                "Regulation Sync Module", 
                "LLM Observability Engine",
                "Narrative Explainability & Replay",
                "Failure Detection & Alert System",
                "Bias & Dataset Tracker",
                "Synthetic Testing Sandbox"
            ]
        })
    
    @app.route('/api/features')
    def list_features():
        """List all available features"""
        return jsonify({
            "features": {
                "1": {
                    "name": "ZenThera Compliance Grid (ZCG)",
                    "status": "active",
                    "endpoints": 8,
                    "description": "Central compliance dashboard with metrics, alerts and automated reporting"
                },
                "2": {
                    "name": "Regulation Sync Module",
                    "status": "active", 
                    "endpoints": 15,
                    "description": "Automated monitoring of AI regulations (AI Act, GDPR) with intelligent alerts"
                },
                "3": {
                    "name": "LLM Observability Engine",
                    "status": "planned",
                    "endpoints": 0,
                    "description": "Advanced LLM monitoring with risk detection and performance analysis"
                },
                "4": {
                    "name": "Narrative Explainability & Replay", 
                    "status": "planned",
                    "endpoints": 0,
                    "description": "Session replay and narrative explanations for audit purposes"
                },
                "5": {
                    "name": "Failure Detection & Alert System",
                    "status": "planned", 
                    "endpoints": 0,
                    "description": "Advanced failure detection with real-time alerts"
                },
                "6": {
                    "name": "Bias & Dataset Tracker",
                    "status": "planned",
                    "endpoints": 0, 
                    "description": "Bias tracking and mitigation in datasets and models"
                },
                "7": {
                    "name": "Synthetic Testing Sandbox",
                    "status": "planned",
                    "endpoints": 0,
                    "description": "Synthetic testing environment for regulatory validation"
                }
            },
            "total_features": 7,
            "active_features": 2,
            "total_endpoints": 23
        })

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

