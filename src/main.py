from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os

# Import route modules
from routes.compliance import compliance_bp
from routes.regulation import regulation_bp
from routes.llm_observability import llm_observability_bp
from routes.narrative_explainability import narrative_explainability_bp
from routes.failure_detection import failure_detection_bp

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
    app.register_blueprint(llm_observability_bp, url_prefix='/api/llm-observability')
    app.register_blueprint(narrative_explainability_bp, url_prefix='/api/narrative-explainability')
    app.register_blueprint(failure_detection_bp, url_prefix='/api/failure-detection')
    
    @app.route('/')
    def index():
        """Main dashboard route"""
        return render_template('index.html')
    
    @app.route('/regulation')
    def regulation_dashboard():
        """Regulation Sync Module dashboard"""
        return render_template('regulation.html')
    
    @app.route('/llm-observability')
    def llm_observability_dashboard():
        """LLM Observability Engine dashboard"""
        return render_template('llm_observability.html')
    
    @app.route('/narrative-explainability')
    def narrative_explainability_dashboard():
        """Narrative Explainability & Replay dashboard"""
        return render_template('narrative_explainability.html')
    
    @app.route('/failure-detection')
    def failure_detection_dashboard():
        """Failure Detection & Alert System dashboard"""
        return render_template('failure_detection.html')
    
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
                    "description": "Central compliance dashboard with metrics, alerts and automated reporting",
                    "url": "/api/compliance"
                },
                "2": {
                    "name": "Regulation Sync Module",
                    "status": "active", 
                    "endpoints": 15,
                    "description": "Automated monitoring of AI regulations (AI Act, GDPR) with intelligent alerts",
                    "url": "/api/regulation"
                },
                "3": {
                    "name": "LLM Observability Engine",
                    "status": "active",
                    "endpoints": 18,
                    "description": "Advanced LLM monitoring with risk detection, quality assessment, and performance analytics",
                    "url": "/api/llm-observability"
                },
                "4": {
                    "name": "Narrative Explainability & Replay", 
                    "status": "active",
                    "endpoints": 16,
                    "description": "Session replay and narrative explanations for audit purposes",
                    "url": "/api/narrative-explainability"
                },
                "5": {
                    "name": "Failure Detection & Alert System", 
                    "status": "active",
                    "endpoints": 14,
                    "description": "Advanced failure detection with real-time alerts and incident management",
                    "url": "/api/failure-detection"
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
            "active_features": 5,
            "total_endpoints": 71,
            "last_updated": "2025-07-18T14:30:00Z"
        })
    
    @app.route('/api/overview')
    def platform_overview():
        """Platform overview with aggregated metrics"""
        return jsonify({
            "platform": {
                "name": "ZenThera AI Ethics Platform",
                "version": "1.0.0",
                "description": "Comprehensive AI Ethics & Governance platform for AI Act compliance"
            },
            "metrics": {
                "total_organizations": 1,
                "total_users": 5,
                "total_ai_models_monitored": 4,
                "total_interactions_processed": 1247,
                "total_risks_detected": 23,
                "total_compliance_reports": 12,
                "total_regulations_monitored": 12,
                "total_session_replays": 47,
                "total_explanations_generated": 156,
                "total_ethical_assessments": 89,
                "total_audit_trails": 23,
                "total_failures_detected": 2,
                "total_alerts_generated": 3,
                "total_incidents_created": 1,
                "system_health_score": 0.73,
                "average_compliance_score": 0.87,
                "average_quality_score": 0.847,
                "average_ethical_alignment": 0.73,
                "average_response_time": "1.2s"
            },
            "features_status": {
                "compliance_grid": "active",
                "regulation_sync": "active",
                "llm_observability": "active",
                "narrative_explainability": "active",
                "failure_detection": "active",
                "bias_tracker": "planned",
                "testing_sandbox": "planned"
            },
            "recent_activity": [
                {
                    "timestamp": "2025-07-18T14:25:00Z",
                    "type": "failure_detected",
                    "description": "Model degradation detected - accuracy dropped 15%",
                    "severity": "high"
                },
                {
                    "timestamp": "2025-07-18T14:23:00Z",
                    "type": "alert_triggered",
                    "description": "Critical error rate spike alert triggered",
                    "severity": "critical"
                },
                {
                    "timestamp": "2025-07-18T14:22:00Z",
                    "type": "incident_created",
                    "description": "Major incident created for model performance degradation",
                    "severity": "high"
                },
                {
                    "timestamp": "2025-07-18T14:22:00Z",
                    "type": "session_replay",
                    "description": "Privacy violation replay created for audit review",
                    "severity": "high"
                },
                {
                    "timestamp": "2025-07-18T14:20:00Z",
                    "type": "regulation_update",
                    "description": "AI Act Article 6 amendment detected",
                    "severity": "critical"
                },
                {
                    "timestamp": "2025-07-18T14:15:00Z",
                    "type": "compliance_report",
                    "description": "Weekly compliance report generated",
                    "severity": "info"
                }
            ]
        })

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

