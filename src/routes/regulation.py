"""
ZenThera AI Ethics Platform
Feature 2: Regulation Sync Module - API Routes

This module provides REST API endpoints for managing regulatory compliance,
including regulation tracking, alerts, templates, and monitoring.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional

# Import our models
from models.regulation import (
    Regulation, RegulatoryAlert, RegulatoryTemplate, RegulationMonitor,
    create_sample_regulations, create_sample_templates
)

# Create Blueprint for regulation routes
regulation_bp = Blueprint('regulation', __name__, url_prefix='/api/regulation')

# In-memory storage for demo (in production, use proper database)
regulations_db = {}
alerts_db = {}
templates_db = {}
monitors_db = {}

# Initialize with sample data
def initialize_sample_data():
    """Initialize the system with sample regulatory data."""
    global regulations_db, templates_db
    
    # Add sample regulations
    sample_regulations = create_sample_regulations()
    for reg in sample_regulations:
        regulations_db[reg.id] = reg
    
    # Add sample templates
    sample_templates = create_sample_templates()
    for template in sample_templates:
        templates_db[template.id] = template
    
    print(f"Initialized with {len(sample_regulations)} regulations and {len(sample_templates)} templates")

# Initialize sample data when module loads
initialize_sample_data()


@regulation_bp.route('/dashboard', methods=['GET'])
def get_regulation_dashboard():
    """
    Get regulatory dashboard overview.
    Returns summary statistics and recent activity.
    """
    try:
        # Calculate statistics
        total_regulations = len(regulations_db)
        active_alerts = len([a for a in alerts_db.values() if a.status == 'active'])
        active_monitors = len([m for m in monitors_db.values() if m.is_active])
        
        # Get recent alerts (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_alerts = [
            a.to_dict() for a in alerts_db.values() 
            if a.created_at >= thirty_days_ago
        ]
        
        # Get regulation breakdown by type
        reg_breakdown = {}
        for reg in regulations_db.values():
            reg_type = reg.regulation_type
            if reg_type not in reg_breakdown:
                reg_breakdown[reg_type] = 0
            reg_breakdown[reg_type] += 1
        
        # Get alert breakdown by impact level
        alert_breakdown = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for alert in alerts_db.values():
            if alert.impact_level in alert_breakdown:
                alert_breakdown[alert.impact_level] += 1
        
        dashboard_data = {
            "summary": {
                "total_regulations": total_regulations,
                "active_alerts": active_alerts,
                "active_monitors": active_monitors,
                "last_sync": datetime.utcnow().isoformat()
            },
            "regulation_breakdown": reg_breakdown,
            "alert_breakdown": alert_breakdown,
            "recent_alerts": recent_alerts[:10],  # Last 10 alerts
            "compliance_status": {
                "ai_act_ready": calculate_ai_act_readiness(),
                "gdpr_compliant": calculate_gdpr_compliance(),
                "overall_score": calculate_overall_compliance_score()
            }
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/regulations', methods=['GET'])
def get_regulations():
    """
    Get list of regulations with optional filtering.
    Query parameters: type, status, jurisdiction, search
    """
    try:
        # Get query parameters
        reg_type = request.args.get('type')
        status = request.args.get('status')
        jurisdiction = request.args.get('jurisdiction')
        search = request.args.get('search', '').lower()
        
        # Filter regulations
        filtered_regs = []
        for reg in regulations_db.values():
            # Apply filters
            if reg_type and reg.regulation_type != reg_type:
                continue
            if status and reg.status != status:
                continue
            if jurisdiction and reg.jurisdiction != jurisdiction:
                continue
            if search and search not in reg.title.lower() and search not in reg.content.lower():
                continue
            
            filtered_regs.append(reg.to_dict())
        
        # Sort by creation date (newest first)
        filtered_regs.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            "regulations": filtered_regs,
            "total": len(filtered_regs),
            "filters_applied": {
                "type": reg_type,
                "status": status,
                "jurisdiction": jurisdiction,
                "search": search
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/regulations/<regulation_id>', methods=['GET'])
def get_regulation(regulation_id):
    """Get detailed information about a specific regulation."""
    try:
        if regulation_id not in regulations_db:
            return jsonify({"error": "Regulation not found"}), 404
        
        regulation = regulations_db[regulation_id]
        
        # Get related alerts
        related_alerts = [
            a.to_dict() for a in alerts_db.values() 
            if a.regulation_id == regulation_id
        ]
        
        response_data = regulation.to_dict()
        response_data["related_alerts"] = related_alerts
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """
    Get regulatory alerts with optional filtering.
    Query parameters: status, impact_level, type, regulation_id
    """
    try:
        # Get query parameters
        status = request.args.get('status')
        impact_level = request.args.get('impact_level')
        alert_type = request.args.get('type')
        regulation_id = request.args.get('regulation_id')
        
        # Filter alerts
        filtered_alerts = []
        for alert in alerts_db.values():
            # Apply filters
            if status and alert.status != status:
                continue
            if impact_level and alert.impact_level != impact_level:
                continue
            if alert_type and alert.alert_type != alert_type:
                continue
            if regulation_id and alert.regulation_id != regulation_id:
                continue
            
            filtered_alerts.append(alert.to_dict())
        
        # Sort by priority and creation date
        filtered_alerts.sort(key=lambda x: (x['priority'], x['created_at']), reverse=True)
        
        return jsonify({
            "alerts": filtered_alerts,
            "total": len(filtered_alerts),
            "summary": {
                "active": len([a for a in filtered_alerts if a['status'] == 'active']),
                "high_priority": len([a for a in filtered_alerts if a['priority'] <= 2]),
                "action_required": len([a for a in filtered_alerts if a['action_required']])
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/alerts', methods=['POST'])
def create_alert():
    """Create a new regulatory alert."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['regulation_id', 'alert_type', 'title', 'description', 'impact_level']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new alert
        alert = RegulatoryAlert(
            regulation_id=data['regulation_id'],
            alert_type=data['alert_type'],
            title=data['title'],
            description=data['description'],
            impact_level=data['impact_level'],
            affected_systems=data.get('affected_systems', [])
        )
        
        # Set optional fields
        if 'deadline' in data:
            alert.deadline = datetime.fromisoformat(data['deadline'])
        
        # Store alert
        alerts_db[alert.id] = alert
        
        return jsonify(alert.to_dict()), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/alerts/<alert_id>/acknowledge', methods=['PUT'])
def acknowledge_alert(alert_id):
    """Acknowledge a regulatory alert."""
    try:
        if alert_id not in alerts_db:
            return jsonify({"error": "Alert not found"}), 404
        
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        notes = data.get('notes', '')
        
        alert = alerts_db[alert_id]
        alert.acknowledge(user_id, notes)
        
        return jsonify(alert.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/alerts/<alert_id>/resolve', methods=['PUT'])
def resolve_alert(alert_id):
    """Resolve a regulatory alert."""
    try:
        if alert_id not in alerts_db:
            return jsonify({"error": "Alert not found"}), 404
        
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        notes = data.get('notes', '')
        
        alert = alerts_db[alert_id]
        alert.resolve(user_id, notes)
        
        return jsonify(alert.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/templates', methods=['GET'])
def get_templates():
    """
    Get regulatory templates with optional filtering.
    Query parameters: regulation_type, template_type, active_only
    """
    try:
        # Get query parameters
        regulation_type = request.args.get('regulation_type')
        template_type = request.args.get('template_type')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        # Filter templates
        filtered_templates = []
        for template in templates_db.values():
            # Apply filters
            if regulation_type and template.regulation_type != regulation_type:
                continue
            if template_type and template.template_type != template_type:
                continue
            if active_only and not template.is_active:
                continue
            
            filtered_templates.append(template.to_dict())
        
        # Sort by usage count and name
        filtered_templates.sort(key=lambda x: (-x['usage_count'], x['name']))
        
        return jsonify({
            "templates": filtered_templates,
            "total": len(filtered_templates)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """Get detailed information about a specific template."""
    try:
        if template_id not in templates_db:
            return jsonify({"error": "Template not found"}), 404
        
        template = templates_db[template_id]
        template.usage_count += 1  # Increment usage counter
        
        return jsonify(template.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/templates/<template_id>/validate', methods=['POST'])
def validate_template_content(template_id):
    """Validate user content against a template."""
    try:
        if template_id not in templates_db:
            return jsonify({"error": "Template not found"}), 404
        
        data = request.get_json()
        user_content = data.get('content', {})
        
        template = templates_db[template_id]
        validation_result = template.validate_content(user_content)
        
        return jsonify(validation_result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/monitors', methods=['GET'])
def get_monitors():
    """Get regulation monitoring configurations."""
    try:
        org_id = request.args.get('organization_id')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        # Filter monitors
        filtered_monitors = []
        for monitor in monitors_db.values():
            if org_id and monitor.organization_id != org_id:
                continue
            if active_only and not monitor.is_active:
                continue
            
            filtered_monitors.append(monitor.to_dict())
        
        return jsonify({
            "monitors": filtered_monitors,
            "total": len(filtered_monitors)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/monitors', methods=['POST'])
def create_monitor():
    """Create a new regulation monitoring configuration."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'regulation_types', 'sources', 'organization_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new monitor
        monitor = RegulationMonitor(
            name=data['name'],
            regulation_types=data['regulation_types'],
            sources=data['sources'],
            keywords=data.get('keywords', []),
            organization_id=data['organization_id']
        )
        
        # Set optional configuration
        if 'check_frequency' in data:
            monitor.check_frequency = data['check_frequency']
        if 'notification_channels' in data:
            monitor.notification_channels = data['notification_channels']
        if 'notification_threshold' in data:
            monitor.notification_threshold = data['notification_threshold']
        if 'recipients' in data:
            monitor.recipients = data['recipients']
        
        # Store monitor
        monitors_db[monitor.id] = monitor
        
        return jsonify(monitor.to_dict()), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@regulation_bp.route('/sync/eur-lex', methods=['POST'])
def sync_eur_lex():
    """
    Trigger synchronization with EUR-Lex database.
    This would connect to the official EU legal database in production.
    """
    try:
        # In production, this would:
        # 1. Connect to EUR-Lex API
        # 2. Check for new/updated AI Act documents
        # 3. Parse and store changes
        # 4. Generate alerts for significant changes
        
        # For demo, simulate finding updates
        sync_result = {
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
            "documents_checked": 15,
            "new_documents": 2,
            "updated_documents": 1,
            "alerts_generated": 1,
            "next_sync": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
        
        # Create a sample alert for demonstration
        if len(alerts_db) < 5:  # Don't spam alerts
            sample_alert = RegulatoryAlert(
                regulation_id=list(regulations_db.keys())[0],  # Use first regulation
                alert_type="amendment",
                title="AI Act Article 6 Amendment Detected",
                description="New clarification added to Article 6 regarding high-risk AI system classification. Review required for systems in healthcare and transportation sectors.",
                impact_level="high",
                affected_systems=["healthcare_ai", "autonomous_vehicles"]
            )
            alerts_db[sample_alert.id] = sample_alert
            sync_result["sample_alert"] = sample_alert.to_dict()
        
        return jsonify(sync_result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Helper functions for dashboard calculations
def calculate_ai_act_readiness() -> float:
    """Calculate AI Act readiness score (0-100)."""
    # In production, this would analyze actual compliance data
    # For demo, return a realistic score
    return 78.5

def calculate_gdpr_compliance() -> float:
    """Calculate GDPR compliance score (0-100)."""
    # In production, this would analyze actual compliance data
    # For demo, return a realistic score
    return 92.3

def calculate_overall_compliance_score() -> float:
    """Calculate overall regulatory compliance score (0-100)."""
    ai_act_score = calculate_ai_act_readiness()
    gdpr_score = calculate_gdpr_compliance()
    
    # Weighted average (AI Act is more critical for our use case)
    return (ai_act_score * 0.6) + (gdpr_score * 0.4)


# Error handlers
@regulation_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@regulation_bp.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@regulation_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

