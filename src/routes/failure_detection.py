"""
ZenThera AI Ethics Platform
Feature 5: Failure Detection & Alert System - API Routes

This module provides comprehensive APIs for failure detection, alert management,
incident tracking, and system health monitoring.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
import json
from models.failure_detection import (
    FailureDetection, Alert, Incident, MonitoringRule, SystemHealth,
    NotificationTemplate, FailureDetectionEngine, AlertEngine,
    HealthMonitoringEngine, NotificationEngine,
    FailureType, AlertSeverity, AlertStatus, IncidentStatus,
    MonitoringMetric, NotificationChannel
)

failure_detection_bp = Blueprint('failure_detection', __name__)

# In-memory storage for demo (would be replaced with actual database)
failure_detections_db = {}
alerts_db = {}
incidents_db = {}
monitoring_rules_db = {}
system_health_db = {}
notification_templates_db = {}

# Initialize with sample data
def initialize_sample_data():
    """Initialize with realistic sample data for demonstration"""
    
    # Sample failure detection
    failure1 = FailureDetection(
        id="failure_001",
        organization_id="org_demo",
        failure_type=FailureType.MODEL_DEGRADATION,
        detected_at=datetime.now() - timedelta(minutes=30),
        detection_method="threshold",
        affected_component="model",
        component_id="gpt-4-model",
        severity_score=0.75,
        confidence_level=0.88,
        failure_description="Model accuracy dropped by 15% compared to baseline",
        root_cause_analysis="Potential data drift detected in recent inputs",
        impact_assessment="Reduced model accuracy affecting user experience",
        affected_metrics=["accuracy", "f1_score"],
        baseline_values={"accuracy": 0.92, "f1_score": 0.89},
        current_values={"accuracy": 0.78, "f1_score": 0.76},
        deviation_percentage=15.2,
        detection_rules=["model_degradation_threshold"],
        related_failures=[],
        mitigation_suggestions=[
            "Retrain model with recent data",
            "Investigate data quality issues",
            "Consider model rollback if degradation is severe"
        ]
    )
    failure_detections_db[failure1.id] = failure1
    
    failure2 = FailureDetection(
        id="failure_002",
        organization_id="org_demo",
        failure_type=FailureType.LATENCY_SPIKE,
        detected_at=datetime.now() - timedelta(minutes=15),
        detection_method="anomaly_detection",
        affected_component="api",
        component_id="api-gateway",
        severity_score=0.65,
        confidence_level=0.92,
        failure_description="Response time increased by 180% in the last 10 minutes",
        root_cause_analysis="Possible resource contention or downstream service issues",
        impact_assessment="Users experiencing slower response times",
        affected_metrics=["response_time"],
        baseline_values={"response_time": 1.2},
        current_values={"response_time": 3.4},
        deviation_percentage=183.3,
        detection_rules=["latency_spike_anomaly"],
        related_failures=[],
        mitigation_suggestions=[
            "Check resource utilization",
            "Investigate downstream dependencies",
            "Consider scaling resources"
        ]
    )
    failure_detections_db[failure2.id] = failure2
    
    # Sample alerts
    alert1 = AlertEngine.create_alert_from_failure(failure1)
    alert1.acknowledged_at = datetime.now() - timedelta(minutes=20)
    alert1.acknowledged_by = "user_001"
    alert1.status = AlertStatus.INVESTIGATING
    alerts_db[alert1.id] = alert1
    
    alert2 = AlertEngine.create_alert_from_failure(failure2)
    alerts_db[alert2.id] = alert2
    
    alert3 = Alert(
        id="alert_003",
        organization_id="org_demo",
        alert_type="threshold",
        severity=AlertSeverity.CRITICAL,
        status=AlertStatus.OPEN,
        title="Critical Error Rate Spike",
        description="Error rate exceeded 5% threshold - immediate attention required",
        source_failure_id=None,
        source_component="api",
        source_metric="error_rate",
        triggered_at=datetime.now() - timedelta(minutes=5),
        triggered_by="monitoring_rule_003",
        acknowledgment_required=True,
        notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.PAGERDUTY],
        tags=["critical", "error_rate", "api"]
    )
    alerts_db[alert3.id] = alert3
    
    # Sample incident
    incident1 = Incident(
        id="incident_001",
        organization_id="org_demo",
        incident_title="Model Performance Degradation",
        incident_description="Significant drop in model accuracy affecting multiple services",
        status=IncidentStatus.INVESTIGATING,
        severity=AlertSeverity.HIGH,
        priority=2,
        created_at=datetime.now() - timedelta(minutes=25),
        created_by="user_001",
        assigned_to="user_002",
        incident_commander="user_003",
        affected_services=["recommendation_service", "content_moderation"],
        affected_users=1500,
        business_impact="Reduced recommendation quality and content moderation accuracy",
        related_alerts=[alert1.id],
        related_failures=[failure1.id],
        timeline=[
            {
                "timestamp": (datetime.now() - timedelta(minutes=25)).isoformat(),
                "event": "Incident created",
                "description": "Model degradation detected and incident opened",
                "actor": "system"
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=20)).isoformat(),
                "event": "Alert acknowledged",
                "description": "Alert acknowledged by on-call engineer",
                "actor": "user_001"
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "event": "Investigation started",
                "description": "Root cause analysis initiated",
                "actor": "user_002"
            }
        ],
        resolution_steps=[
            "Analyze recent data patterns",
            "Check model training pipeline",
            "Prepare model rollback if necessary"
        ],
        estimated_resolution=datetime.now() + timedelta(hours=2)
    )
    incidents_db[incident1.id] = incident1
    
    # Sample monitoring rules
    rule1 = MonitoringRule(
        id="rule_001",
        organization_id="org_demo",
        rule_name="Model Accuracy Threshold",
        rule_description="Alert when model accuracy drops below 85%",
        is_active=True,
        metric_name=MonitoringMetric.QUALITY_SCORE,
        component_type="model",
        component_filter={"model_type": "classification"},
        threshold_type="static",
        threshold_value=0.85,
        threshold_operator="<",
        baseline_period=24,
        evaluation_window=15,
        sensitivity=0.8,
        failure_type=FailureType.MODEL_DEGRADATION,
        alert_severity=AlertSeverity.HIGH,
        notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
        trigger_count=3,
        false_positive_count=1
    )
    monitoring_rules_db[rule1.id] = rule1
    
    rule2 = MonitoringRule(
        id="rule_002",
        organization_id="org_demo",
        rule_name="Response Time Anomaly",
        rule_description="Detect unusual spikes in response time",
        is_active=True,
        metric_name=MonitoringMetric.RESPONSE_TIME,
        component_type="api",
        component_filter={"service": "main_api"},
        threshold_type="anomaly",
        baseline_period=168,  # 1 week
        evaluation_window=5,
        sensitivity=0.9,
        failure_type=FailureType.LATENCY_SPIKE,
        alert_severity=AlertSeverity.MEDIUM,
        notification_channels=[NotificationChannel.EMAIL],
        trigger_count=1
    )
    monitoring_rules_db[rule2.id] = rule2
    
    # Sample system health
    health1 = HealthMonitoringEngine.calculate_system_health(
        alerts=list(alerts_db.values()),
        incidents=list(incidents_db.values()),
        failures=list(failure_detections_db.values()),
        performance_metrics={
            "response_time": 2.1,
            "error_rate": 0.023,
            "throughput": 145.0,
            "quality_score": 0.82,
            "p95_response_time": 3.8
        }
    )
    system_health_db[health1.id] = health1
    
    # Sample notification templates
    template1 = NotificationTemplate(
        id="template_001",
        organization_id="org_demo",
        template_name="Critical Alert Email",
        template_type="email",
        subject_template="🚨 CRITICAL ALERT: {alert_title}",
        body_template="""
CRITICAL ALERT NOTIFICATION

Alert: {alert_title}
Severity: {severity}
Component: {component}
Triggered: {triggered_at}

Description:
{alert_description}

Alert ID: {alert_id}
Organization: {organization}

Please acknowledge this alert immediately and begin investigation.

ZenThera AI Ethics Platform
        """.strip(),
        variables=["alert_title", "severity", "component", "triggered_at", "alert_description", "alert_id", "organization"],
        formatting_rules={"max_subject_length": 100},
        usage_count=15
    )
    notification_templates_db[template1.id] = template1

# Initialize sample data
initialize_sample_data()


@failure_detection_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get failure detection dashboard data"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        time_range = request.args.get('time_range', '24h')
        
        # Calculate time window
        now = datetime.now()
        if time_range == '1h':
            start_time = now - timedelta(hours=1)
        elif time_range == '24h':
            start_time = now - timedelta(days=1)
        elif time_range == '7d':
            start_time = now - timedelta(days=7)
        else:  # 30d
            start_time = now - timedelta(days=30)
        
        # Filter data by organization and time range
        org_failures = [f for f in failure_detections_db.values() 
                       if f.organization_id == org_id and f.detected_at >= start_time]
        org_alerts = [a for a in alerts_db.values() 
                     if a.organization_id == org_id and a.triggered_at >= start_time]
        org_incidents = [i for i in incidents_db.values() 
                        if i.organization_id == org_id and i.created_at >= start_time]
        
        # Get latest system health
        latest_health = max(system_health_db.values(), key=lambda x: x.timestamp) if system_health_db else None
        
        # Calculate metrics
        total_failures = len(org_failures)
        total_alerts = len(org_alerts)
        total_incidents = len(org_incidents)
        
        # Alert metrics
        open_alerts = len([a for a in org_alerts if a.status == AlertStatus.OPEN])
        critical_alerts = len([a for a in org_alerts if a.severity == AlertSeverity.CRITICAL])
        acknowledged_alerts = len([a for a in org_alerts if a.status == AlertStatus.ACKNOWLEDGED])
        
        # Incident metrics
        open_incidents = len([i for i in org_incidents if i.status not in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]])
        
        # Failure type distribution
        failure_types = {}
        for failure in org_failures:
            failure_type = failure.failure_type.value
            if failure_type not in failure_types:
                failure_types[failure_type] = 0
            failure_types[failure_type] += 1
        
        # Component health
        component_health = latest_health.component_health if latest_health else {}
        
        # Recent activity
        recent_activity = []
        
        # Add recent failures
        for failure in sorted(org_failures, key=lambda x: x.detected_at, reverse=True)[:3]:
            recent_activity.append({
                "timestamp": failure.detected_at.isoformat(),
                "type": "failure_detected",
                "description": f"{failure.failure_type.value.replace('_', ' ').title()} detected in {failure.affected_component}",
                "severity": "high" if failure.severity_score > 0.7 else "medium"
            })
        
        # Add recent alerts
        for alert in sorted(org_alerts, key=lambda x: x.triggered_at, reverse=True)[:2]:
            recent_activity.append({
                "timestamp": alert.triggered_at.isoformat(),
                "type": "alert_triggered",
                "description": alert.title,
                "severity": alert.severity.value
            })
        
        # Sort recent activity by timestamp
        recent_activity.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            "status": "success",
            "data": {
                "overview": {
                    "total_failures_detected": total_failures,
                    "total_alerts_generated": total_alerts,
                    "total_incidents_created": total_incidents,
                    "open_alerts": open_alerts,
                    "critical_alerts": critical_alerts,
                    "acknowledged_alerts": acknowledged_alerts,
                    "open_incidents": open_incidents,
                    "system_health_score": latest_health.overall_health_score if latest_health else 0.85,
                    "availability_percentage": latest_health.availability_percentage if latest_health else 99.5,
                    "mean_response_time": latest_health.mean_response_time if latest_health else 1.2
                },
                "failure_types": failure_types,
                "component_health": component_health,
                "recent_activity": recent_activity[:10],
                "system_health": latest_health.to_dict() if latest_health else None,
                "time_range": time_range,
                "last_updated": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/failures', methods=['GET'])
def get_failures():
    """Get list of detected failures with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        failure_type = request.args.get('failure_type')
        component = request.args.get('component')
        min_severity = float(request.args.get('min_severity', 0.0))
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Filter failures
        filtered_failures = []
        for failure in failure_detections_db.values():
            if failure.organization_id != org_id:
                continue
            if failure_type and failure.failure_type.value != failure_type:
                continue
            if component and failure.affected_component != component:
                continue
            if failure.severity_score < min_severity:
                continue
            
            filtered_failures.append(failure)
        
        # Sort by detection time (newest first)
        filtered_failures.sort(key=lambda x: x.detected_at, reverse=True)
        
        # Apply pagination
        total_count = len(filtered_failures)
        paginated_failures = filtered_failures[offset:offset + limit]
        
        return jsonify({
            "status": "success",
            "data": {
                "failures": [f.to_dict() for f in paginated_failures],
                "pagination": {
                    "total_count": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "summary": {
                    "total_failures": total_count,
                    "by_type": {
                        failure_type.value: len([f for f in filtered_failures if f.failure_type == failure_type])
                        for failure_type in FailureType
                    },
                    "by_component": {
                        "model": len([f for f in filtered_failures if f.affected_component == "model"]),
                        "api": len([f for f in filtered_failures if f.affected_component == "api"]),
                        "pipeline": len([f for f in filtered_failures if f.affected_component == "pipeline"]),
                        "integration": len([f for f in filtered_failures if f.affected_component == "integration"])
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/failures', methods=['POST'])
def detect_failure():
    """Manually trigger failure detection or report a failure"""
    try:
        data = request.get_json()
        
        # Create failure detection record
        failure = FailureDetection(
            id=str(uuid.uuid4()),
            organization_id=data['organization_id'],
            failure_type=FailureType(data['failure_type']),
            detected_at=datetime.now(),
            detection_method=data.get('detection_method', 'manual'),
            affected_component=data['affected_component'],
            component_id=data['component_id'],
            severity_score=data['severity_score'],
            confidence_level=data.get('confidence_level', 0.8),
            failure_description=data['failure_description'],
            root_cause_analysis=data.get('root_cause_analysis', ''),
            impact_assessment=data.get('impact_assessment', ''),
            affected_metrics=data.get('affected_metrics', []),
            baseline_values=data.get('baseline_values', {}),
            current_values=data.get('current_values', {}),
            deviation_percentage=data.get('deviation_percentage', 0.0),
            detection_rules=data.get('detection_rules', []),
            related_failures=data.get('related_failures', []),
            mitigation_suggestions=data.get('mitigation_suggestions', [])
        )
        
        failure_detections_db[failure.id] = failure
        
        # Auto-create alert if severity is high enough
        if failure.severity_score >= 0.5:
            alert = AlertEngine.create_alert_from_failure(failure)
            alerts_db[alert.id] = alert
            
            return jsonify({
                "status": "success",
                "data": {
                    "failure": failure.to_dict(),
                    "alert_created": alert.to_dict(),
                    "message": "Failure detected and alert created"
                }
            }), 201
        else:
            return jsonify({
                "status": "success",
                "data": {
                    "failure": failure.to_dict(),
                    "alert_created": None,
                    "message": "Failure detected (no alert created due to low severity)"
                }
            }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get list of alerts with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        severity = request.args.get('severity')
        status = request.args.get('status')
        component = request.args.get('component')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Filter alerts
        filtered_alerts = []
        for alert in alerts_db.values():
            if alert.organization_id != org_id:
                continue
            if severity and alert.severity.value != severity:
                continue
            if status and alert.status.value != status:
                continue
            if component and alert.source_component != component:
                continue
            
            filtered_alerts.append(alert)
        
        # Sort by trigger time (newest first)
        filtered_alerts.sort(key=lambda x: x.triggered_at, reverse=True)
        
        # Apply pagination
        total_count = len(filtered_alerts)
        paginated_alerts = filtered_alerts[offset:offset + limit]
        
        # Enrich alerts with additional information
        enriched_alerts = []
        for alert in paginated_alerts:
            alert_dict = alert.to_dict()
            
            # Add related failure information
            if alert.source_failure_id and alert.source_failure_id in failure_detections_db:
                failure = failure_detections_db[alert.source_failure_id]
                alert_dict['related_failure'] = {
                    "id": failure.id,
                    "type": failure.failure_type.value,
                    "severity_score": failure.severity_score,
                    "affected_metrics": failure.affected_metrics
                }
            
            # Calculate alert age
            alert_age = (datetime.now() - alert.triggered_at).total_seconds() / 60  # Minutes
            alert_dict['age_minutes'] = alert_age
            
            enriched_alerts.append(alert_dict)
        
        return jsonify({
            "status": "success",
            "data": {
                "alerts": enriched_alerts,
                "pagination": {
                    "total_count": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "summary": {
                    "total_alerts": total_count,
                    "by_severity": {
                        severity.value: len([a for a in filtered_alerts if a.severity == severity])
                        for severity in AlertSeverity
                    },
                    "by_status": {
                        status.value: len([a for a in filtered_alerts if a.status == status])
                        for status in AlertStatus
                    },
                    "requires_acknowledgment": len([a for a in filtered_alerts 
                                                  if a.acknowledgment_required and a.status == AlertStatus.OPEN])
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    try:
        if alert_id not in alerts_db:
            return jsonify({"status": "error", "message": "Alert not found"}), 404
        
        data = request.get_json()
        alert = alerts_db[alert_id]
        
        if alert.status != AlertStatus.OPEN:
            return jsonify({"status": "error", "message": "Alert is not in open status"}), 400
        
        # Update alert
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = datetime.now()
        alert.acknowledged_by = data.get('acknowledged_by', 'unknown')
        
        # Add to notification history
        alert.notification_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "acknowledged",
            "actor": alert.acknowledged_by,
            "notes": data.get('notes', '')
        })
        
        return jsonify({
            "status": "success",
            "data": {
                "alert": alert.to_dict(),
                "message": "Alert acknowledged successfully"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve an alert"""
    try:
        if alert_id not in alerts_db:
            return jsonify({"status": "error", "message": "Alert not found"}), 404
        
        data = request.get_json()
        alert = alerts_db[alert_id]
        
        if alert.status in [AlertStatus.RESOLVED, AlertStatus.CLOSED]:
            return jsonify({"status": "error", "message": "Alert is already resolved"}), 400
        
        # Update alert
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = datetime.now()
        alert.resolved_by = data.get('resolved_by', 'unknown')
        alert.resolution_notes = data.get('resolution_notes', '')
        
        # Add to notification history
        alert.notification_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "resolved",
            "actor": alert.resolved_by,
            "notes": alert.resolution_notes
        })
        
        return jsonify({
            "status": "success",
            "data": {
                "alert": alert.to_dict(),
                "message": "Alert resolved successfully"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/incidents', methods=['GET'])
def get_incidents():
    """Get list of incidents with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        status = request.args.get('status')
        severity = request.args.get('severity')
        limit = int(request.args.get('limit', 50))
        
        # Filter incidents
        filtered_incidents = []
        for incident in incidents_db.values():
            if incident.organization_id != org_id:
                continue
            if status and incident.status.value != status:
                continue
            if severity and incident.severity.value != severity:
                continue
            
            filtered_incidents.append(incident)
        
        # Sort by creation time (newest first)
        filtered_incidents.sort(key=lambda x: x.created_at, reverse=True)
        
        # Apply limit
        limited_incidents = filtered_incidents[:limit]
        
        return jsonify({
            "status": "success",
            "data": {
                "incidents": [i.to_dict() for i in limited_incidents],
                "summary": {
                    "total_incidents": len(filtered_incidents),
                    "by_status": {
                        status.value: len([i for i in filtered_incidents if i.status == status])
                        for status in IncidentStatus
                    },
                    "by_severity": {
                        severity.value: len([i for i in filtered_incidents if i.severity == severity])
                        for severity in AlertSeverity
                    },
                    "open_incidents": len([i for i in filtered_incidents 
                                         if i.status not in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]])
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/incidents', methods=['POST'])
def create_incident():
    """Create a new incident"""
    try:
        data = request.get_json()
        
        incident = Incident(
            id=str(uuid.uuid4()),
            organization_id=data['organization_id'],
            incident_title=data['incident_title'],
            incident_description=data['incident_description'],
            status=IncidentStatus.DETECTED,
            severity=AlertSeverity(data['severity']),
            priority=data.get('priority', 3),
            created_at=datetime.now(),
            created_by=data['created_by'],
            assigned_to=data.get('assigned_to'),
            incident_commander=data.get('incident_commander'),
            affected_services=data.get('affected_services', []),
            affected_users=data.get('affected_users', 0),
            business_impact=data.get('business_impact', ''),
            related_alerts=data.get('related_alerts', []),
            related_failures=data.get('related_failures', []),
            estimated_resolution=datetime.fromisoformat(data['estimated_resolution']) if data.get('estimated_resolution') else None
        )
        
        # Add initial timeline entry
        incident.timeline.append({
            "timestamp": incident.created_at.isoformat(),
            "event": "Incident created",
            "description": "Incident opened and initial assessment started",
            "actor": incident.created_by
        })
        
        incidents_db[incident.id] = incident
        
        return jsonify({
            "status": "success",
            "data": {
                "incident": incident.to_dict(),
                "message": "Incident created successfully"
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/monitoring-rules', methods=['GET'])
def get_monitoring_rules():
    """Get list of monitoring rules"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        is_active = request.args.get('is_active')
        component_type = request.args.get('component_type')
        
        # Filter rules
        filtered_rules = []
        for rule in monitoring_rules_db.values():
            if rule.organization_id != org_id:
                continue
            if is_active is not None and rule.is_active != (is_active.lower() == 'true'):
                continue
            if component_type and rule.component_type != component_type:
                continue
            
            filtered_rules.append(rule)
        
        # Sort by creation time (newest first)
        filtered_rules.sort(key=lambda x: x.created_at, reverse=True)
        
        return jsonify({
            "status": "success",
            "data": {
                "monitoring_rules": [r.to_dict() for r in filtered_rules],
                "summary": {
                    "total_rules": len(filtered_rules),
                    "active_rules": len([r for r in filtered_rules if r.is_active]),
                    "by_component": {
                        "model": len([r for r in filtered_rules if r.component_type == "model"]),
                        "api": len([r for r in filtered_rules if r.component_type == "api"]),
                        "pipeline": len([r for r in filtered_rules if r.component_type == "pipeline"])
                    },
                    "by_metric": {
                        metric.value: len([r for r in filtered_rules if r.metric_name == metric])
                        for metric in MonitoringMetric
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/monitoring-rules', methods=['POST'])
def create_monitoring_rule():
    """Create a new monitoring rule"""
    try:
        data = request.get_json()
        
        rule = MonitoringRule(
            id=str(uuid.uuid4()),
            organization_id=data['organization_id'],
            rule_name=data['rule_name'],
            rule_description=data['rule_description'],
            is_active=data.get('is_active', True),
            metric_name=MonitoringMetric(data['metric_name']),
            component_type=data['component_type'],
            component_filter=data.get('component_filter', {}),
            threshold_type=data['threshold_type'],
            threshold_value=data.get('threshold_value'),
            threshold_operator=data.get('threshold_operator', '>'),
            baseline_period=data.get('baseline_period', 24),
            evaluation_window=data.get('evaluation_window', 5),
            sensitivity=data.get('sensitivity', 0.8),
            min_data_points=data.get('min_data_points', 3),
            failure_type=FailureType(data.get('failure_type', 'performance_anomaly')),
            alert_severity=AlertSeverity(data.get('alert_severity', 'medium')),
            notification_channels=[NotificationChannel(ch) for ch in data.get('notification_channels', ['email'])],
            suppression_duration=data.get('suppression_duration', 60),
            escalation_rules=data.get('escalation_rules', []),
            created_by=data.get('created_by', 'system')
        )
        
        monitoring_rules_db[rule.id] = rule
        
        return jsonify({
            "status": "success",
            "data": {
                "monitoring_rule": rule.to_dict(),
                "message": "Monitoring rule created successfully"
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/system-health', methods=['GET'])
def get_system_health():
    """Get current system health status"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        
        # Get latest health record
        org_health_records = [h for h in system_health_db.values() if h.organization_id == org_id]
        
        if not org_health_records:
            # Calculate current health if no records exist
            current_health = HealthMonitoringEngine.calculate_system_health(
                alerts=list(alerts_db.values()),
                incidents=list(incidents_db.values()),
                failures=list(failure_detections_db.values()),
                performance_metrics={
                    "response_time": 1.2,
                    "error_rate": 0.015,
                    "throughput": 150.0,
                    "quality_score": 0.85
                }
            )
            system_health_db[current_health.id] = current_health
        else:
            current_health = max(org_health_records, key=lambda x: x.timestamp)
        
        return jsonify({
            "status": "success",
            "data": {
                "system_health": current_health.to_dict(),
                "health_status": {
                    "overall": "healthy" if current_health.overall_health_score >= 0.8 else 
                              "degraded" if current_health.overall_health_score >= 0.6 else "unhealthy",
                    "components": {
                        component: "healthy" if score >= 0.8 else "degraded" if score >= 0.6 else "unhealthy"
                        for component, score in current_health.component_health.items()
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/system-health/history', methods=['GET'])
def get_system_health_history():
    """Get system health history"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        hours = int(request.args.get('hours', 24))
        
        # Filter health records
        start_time = datetime.now() - timedelta(hours=hours)
        health_records = [h for h in system_health_db.values() 
                         if h.organization_id == org_id and h.timestamp >= start_time]
        
        # Sort by timestamp
        health_records.sort(key=lambda x: x.timestamp)
        
        return jsonify({
            "status": "success",
            "data": {
                "health_history": [h.to_dict() for h in health_records],
                "time_range_hours": hours,
                "data_points": len(health_records)
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@failure_detection_bp.route('/simulate-failure', methods=['POST'])
def simulate_failure():
    """Simulate a failure for testing purposes"""
    try:
        data = request.get_json()
        
        # Simulate different types of failures based on request
        simulation_type = data.get('simulation_type', 'model_degradation')
        
        if simulation_type == 'model_degradation':
            failure = FailureDetectionEngine.detect_model_degradation(
                current_metrics={"accuracy": 0.75, "f1_score": 0.72},
                baseline_metrics={"accuracy": 0.92, "f1_score": 0.89}
            )
        elif simulation_type == 'latency_spike':
            failure = FailureDetectionEngine.detect_latency_spike(
                current_latency=4.5,
                baseline_latency=1.2
            )
        elif simulation_type == 'error_rate_increase':
            failure = FailureDetectionEngine.detect_error_rate_increase(
                current_error_rate=0.08,
                baseline_error_rate=0.01
            )
        else:
            return jsonify({"status": "error", "message": "Unknown simulation type"}), 400
        
        if failure:
            failure_detections_db[failure.id] = failure
            
            # Create alert
            alert = AlertEngine.create_alert_from_failure(failure)
            alerts_db[alert.id] = alert
            
            return jsonify({
                "status": "success",
                "data": {
                    "simulation_type": simulation_type,
                    "failure": failure.to_dict(),
                    "alert": alert.to_dict(),
                    "message": f"Successfully simulated {simulation_type}"
                }
            })
        else:
            return jsonify({
                "status": "success",
                "data": {
                    "simulation_type": simulation_type,
                    "failure": None,
                    "message": f"Simulation ran but no failure detected for {simulation_type}"
                }
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

