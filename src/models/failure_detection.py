"""
ZenThera AI Ethics Platform
Feature 5: Failure Detection & Alert System - Data Models

This module defines the data models for failure detection, alert management,
incident tracking, and proactive monitoring of AI system health.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json
import uuid


class FailureType(Enum):
    """Types of failures that can be detected"""
    MODEL_DEGRADATION = "model_degradation"
    PERFORMANCE_ANOMALY = "performance_anomaly"
    QUALITY_DROP = "quality_drop"
    LATENCY_SPIKE = "latency_spike"
    ERROR_RATE_INCREASE = "error_rate_increase"
    BIAS_DRIFT = "bias_drift"
    SAFETY_VIOLATION = "safety_violation"
    COMPLIANCE_BREACH = "compliance_breach"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    INTEGRATION_FAILURE = "integration_failure"
    DATA_PIPELINE_FAILURE = "data_pipeline_failure"
    SECURITY_INCIDENT = "security_incident"


class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"  # Immediate action required
    HIGH = "high"         # Action required within hours
    MEDIUM = "medium"     # Action required within days
    LOW = "low"          # Informational, no immediate action
    INFO = "info"        # General information


class AlertStatus(Enum):
    """Alert status lifecycle"""
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"
    SUPPRESSED = "suppressed"


class IncidentStatus(Enum):
    """Incident status lifecycle"""
    DETECTED = "detected"
    TRIAGING = "triaging"
    INVESTIGATING = "investigating"
    MITIGATING = "mitigating"
    RESOLVED = "resolved"
    POST_MORTEM = "post_mortem"
    CLOSED = "closed"


class MonitoringMetric(Enum):
    """Metrics being monitored for failures"""
    RESPONSE_TIME = "response_time"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    QUALITY_SCORE = "quality_score"
    BIAS_SCORE = "bias_score"
    SAFETY_SCORE = "safety_score"
    COMPLIANCE_SCORE = "compliance_score"
    RESOURCE_USAGE = "resource_usage"
    USER_SATISFACTION = "user_satisfaction"
    MODEL_CONFIDENCE = "model_confidence"


class NotificationChannel(Enum):
    """Notification delivery channels"""
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    WEBHOOK = "webhook"
    SMS = "sms"
    PAGERDUTY = "pagerduty"
    DASHBOARD = "dashboard"


@dataclass
class FailureDetection:
    """Detected failure or anomaly in the system"""
    id: str
    organization_id: str
    failure_type: FailureType
    detected_at: datetime
    detection_method: str  # "threshold", "anomaly_detection", "ml_model", "rule_based"
    affected_component: str  # "model", "api", "pipeline", "integration"
    component_id: str
    severity_score: float  # 0.0 to 1.0
    confidence_level: float  # 0.0 to 1.0
    failure_description: str
    root_cause_analysis: str
    impact_assessment: str
    affected_metrics: List[str]
    baseline_values: Dict[str, float]
    current_values: Dict[str, float]
    deviation_percentage: float
    detection_rules: List[str]
    related_failures: List[str]  # IDs of related failures
    mitigation_suggestions: List[str]
    is_false_positive: bool = False
    false_positive_reason: str = ""
    detection_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "failure_type": self.failure_type.value,
            "detected_at": self.detected_at.isoformat(),
            "detection_method": self.detection_method,
            "affected_component": self.affected_component,
            "component_id": self.component_id,
            "severity_score": self.severity_score,
            "confidence_level": self.confidence_level,
            "failure_description": self.failure_description,
            "root_cause_analysis": self.root_cause_analysis,
            "impact_assessment": self.impact_assessment,
            "affected_metrics": self.affected_metrics,
            "baseline_values": self.baseline_values,
            "current_values": self.current_values,
            "deviation_percentage": self.deviation_percentage,
            "detection_rules": self.detection_rules,
            "related_failures": self.related_failures,
            "mitigation_suggestions": self.mitigation_suggestions,
            "is_false_positive": self.is_false_positive,
            "false_positive_reason": self.false_positive_reason,
            "detection_metadata": self.detection_metadata
        }


@dataclass
class Alert:
    """Alert generated from failure detection or monitoring"""
    id: str
    organization_id: str
    alert_type: str  # "failure", "threshold", "anomaly", "compliance"
    severity: AlertSeverity
    status: AlertStatus
    title: str
    description: str
    source_failure_id: Optional[str]  # Related failure detection ID
    source_component: str
    source_metric: Optional[str]
    triggered_at: datetime
    triggered_by: str  # "system", "user_id", "rule_id"
    acknowledgment_required: bool
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolution_notes: str = ""
    escalation_level: int = 0  # 0 = initial, 1+ = escalated
    escalation_history: List[Dict[str, Any]] = field(default_factory=list)
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    notification_history: List[Dict[str, Any]] = field(default_factory=list)
    suppression_rules: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    alert_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "alert_type": self.alert_type,
            "severity": self.severity.value,
            "status": self.status.value,
            "title": self.title,
            "description": self.description,
            "source_failure_id": self.source_failure_id,
            "source_component": self.source_component,
            "source_metric": self.source_metric,
            "triggered_at": self.triggered_at.isoformat(),
            "triggered_by": self.triggered_by,
            "acknowledgment_required": self.acknowledgment_required,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "acknowledged_by": self.acknowledged_by,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "resolution_notes": self.resolution_notes,
            "escalation_level": self.escalation_level,
            "escalation_history": self.escalation_history,
            "notification_channels": [ch.value for ch in self.notification_channels],
            "notification_history": self.notification_history,
            "suppression_rules": self.suppression_rules,
            "tags": self.tags,
            "alert_metadata": self.alert_metadata
        }


@dataclass
class Incident:
    """Major incident requiring coordinated response"""
    id: str
    organization_id: str
    incident_title: str
    incident_description: str
    status: IncidentStatus
    severity: AlertSeverity
    priority: int  # 1 = highest, 5 = lowest
    created_at: datetime
    created_by: str
    assigned_to: Optional[str] = None
    incident_commander: Optional[str] = None
    affected_services: List[str] = field(default_factory=list)
    affected_users: int = 0
    business_impact: str = ""
    related_alerts: List[str] = field(default_factory=list)
    related_failures: List[str] = field(default_factory=list)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    resolution_steps: List[str] = field(default_factory=list)
    root_cause: str = ""
    lessons_learned: str = ""
    post_mortem_url: str = ""
    estimated_resolution: Optional[datetime] = None
    actual_resolution: Optional[datetime] = None
    communication_updates: List[Dict[str, Any]] = field(default_factory=list)
    incident_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "incident_title": self.incident_title,
            "incident_description": self.incident_description,
            "status": self.status.value,
            "severity": self.severity.value,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "assigned_to": self.assigned_to,
            "incident_commander": self.incident_commander,
            "affected_services": self.affected_services,
            "affected_users": self.affected_users,
            "business_impact": self.business_impact,
            "related_alerts": self.related_alerts,
            "related_failures": self.related_failures,
            "timeline": self.timeline,
            "resolution_steps": self.resolution_steps,
            "root_cause": self.root_cause,
            "lessons_learned": self.lessons_learned,
            "post_mortem_url": self.post_mortem_url,
            "estimated_resolution": self.estimated_resolution.isoformat() if self.estimated_resolution else None,
            "actual_resolution": self.actual_resolution.isoformat() if self.actual_resolution else None,
            "communication_updates": self.communication_updates,
            "incident_metadata": self.incident_metadata
        }


@dataclass
class MonitoringRule:
    """Rule for monitoring metrics and detecting failures"""
    id: str
    organization_id: str
    rule_name: str
    rule_description: str
    is_active: bool
    metric_name: MonitoringMetric
    component_type: str  # "model", "api", "pipeline"
    component_filter: Dict[str, Any]  # Filters to apply
    threshold_type: str  # "static", "dynamic", "anomaly"
    threshold_value: Optional[float] = None
    threshold_operator: str = ">"  # ">", "<", ">=", "<=", "==", "!="
    baseline_period: int = 24  # Hours for baseline calculation
    evaluation_window: int = 5  # Minutes for evaluation
    sensitivity: float = 0.8  # 0.0 to 1.0
    min_data_points: int = 3
    failure_type: FailureType = FailureType.PERFORMANCE_ANOMALY
    alert_severity: AlertSeverity = AlertSeverity.MEDIUM
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    suppression_duration: int = 60  # Minutes to suppress duplicate alerts
    escalation_rules: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0
    false_positive_count: int = 0
    rule_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "rule_name": self.rule_name,
            "rule_description": self.rule_description,
            "is_active": self.is_active,
            "metric_name": self.metric_name.value,
            "component_type": self.component_type,
            "component_filter": self.component_filter,
            "threshold_type": self.threshold_type,
            "threshold_value": self.threshold_value,
            "threshold_operator": self.threshold_operator,
            "baseline_period": self.baseline_period,
            "evaluation_window": self.evaluation_window,
            "sensitivity": self.sensitivity,
            "min_data_points": self.min_data_points,
            "failure_type": self.failure_type.value,
            "alert_severity": self.alert_severity.value,
            "notification_channels": [ch.value for ch in self.notification_channels],
            "suppression_duration": self.suppression_duration,
            "escalation_rules": self.escalation_rules,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "trigger_count": self.trigger_count,
            "false_positive_count": self.false_positive_count,
            "rule_metadata": self.rule_metadata
        }


@dataclass
class SystemHealth:
    """Overall system health status"""
    id: str
    organization_id: str
    timestamp: datetime
    overall_health_score: float  # 0.0 to 1.0
    component_health: Dict[str, float]  # Component -> health score
    active_alerts_count: int
    critical_alerts_count: int
    open_incidents_count: int
    recent_failures_count: int
    performance_metrics: Dict[str, float]
    availability_percentage: float
    error_rate_percentage: float
    mean_response_time: float
    p95_response_time: float
    throughput_per_minute: float
    resource_utilization: Dict[str, float]
    trend_analysis: Dict[str, str]  # Metric -> "improving", "stable", "degrading"
    health_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "timestamp": self.timestamp.isoformat(),
            "overall_health_score": self.overall_health_score,
            "component_health": self.component_health,
            "active_alerts_count": self.active_alerts_count,
            "critical_alerts_count": self.critical_alerts_count,
            "open_incidents_count": self.open_incidents_count,
            "recent_failures_count": self.recent_failures_count,
            "performance_metrics": self.performance_metrics,
            "availability_percentage": self.availability_percentage,
            "error_rate_percentage": self.error_rate_percentage,
            "mean_response_time": self.mean_response_time,
            "p95_response_time": self.p95_response_time,
            "throughput_per_minute": self.throughput_per_minute,
            "resource_utilization": self.resource_utilization,
            "trend_analysis": self.trend_analysis,
            "health_metadata": self.health_metadata
        }


@dataclass
class NotificationTemplate:
    """Template for alert notifications"""
    id: str
    organization_id: str
    template_name: str
    template_type: str  # "email", "slack", "teams", "webhook"
    subject_template: str
    body_template: str
    variables: List[str]  # Available template variables
    formatting_rules: Dict[str, Any]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    usage_count: int = 0
    template_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "template_name": self.template_name,
            "template_type": self.template_type,
            "subject_template": self.subject_template,
            "body_template": self.body_template,
            "variables": self.variables,
            "formatting_rules": self.formatting_rules,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "usage_count": self.usage_count,
            "template_metadata": self.template_metadata
        }


# Failure Detection Engine
class FailureDetectionEngine:
    """Advanced engine for detecting various types of failures"""
    
    @staticmethod
    def detect_model_degradation(current_metrics: Dict[str, float], 
                                baseline_metrics: Dict[str, float],
                                threshold: float = 0.1) -> Optional[FailureDetection]:
        """Detect model performance degradation"""
        
        degradation_score = 0.0
        affected_metrics = []
        current_values = {}
        baseline_values = {}
        
        # Check key performance metrics
        key_metrics = ['quality_score', 'accuracy', 'f1_score', 'precision', 'recall']
        
        for metric in key_metrics:
            if metric in current_metrics and metric in baseline_metrics:
                current_val = current_metrics[metric]
                baseline_val = baseline_metrics[metric]
                
                if baseline_val > 0:
                    degradation = (baseline_val - current_val) / baseline_val
                    if degradation > threshold:
                        degradation_score += degradation
                        affected_metrics.append(metric)
                        current_values[metric] = current_val
                        baseline_values[metric] = baseline_val
        
        if degradation_score > threshold:
            return FailureDetection(
                id=str(uuid.uuid4()),
                organization_id="org_demo",
                failure_type=FailureType.MODEL_DEGRADATION,
                detected_at=datetime.now(),
                detection_method="threshold",
                affected_component="model",
                component_id="model_001",
                severity_score=min(degradation_score, 1.0),
                confidence_level=0.85,
                failure_description=f"Model performance degraded by {degradation_score*100:.1f}%",
                root_cause_analysis="Potential data drift or model staleness detected",
                impact_assessment="Reduced model accuracy may affect user experience",
                affected_metrics=affected_metrics,
                baseline_values=baseline_values,
                current_values=current_values,
                deviation_percentage=degradation_score * 100,
                detection_rules=["model_degradation_threshold"],
                related_failures=[],
                mitigation_suggestions=[
                    "Retrain model with recent data",
                    "Investigate data quality issues",
                    "Consider model rollback if degradation is severe"
                ]
            )
        
        return None
    
    @staticmethod
    def detect_latency_spike(current_latency: float, 
                           baseline_latency: float,
                           spike_threshold: float = 2.0) -> Optional[FailureDetection]:
        """Detect response time spikes"""
        
        if baseline_latency > 0:
            latency_ratio = current_latency / baseline_latency
            
            if latency_ratio > spike_threshold:
                severity = min((latency_ratio - 1.0) / 3.0, 1.0)  # Normalize to 0-1
                
                return FailureDetection(
                    id=str(uuid.uuid4()),
                    organization_id="org_demo",
                    failure_type=FailureType.LATENCY_SPIKE,
                    detected_at=datetime.now(),
                    detection_method="threshold",
                    affected_component="api",
                    component_id="api_001",
                    severity_score=severity,
                    confidence_level=0.9,
                    failure_description=f"Response time increased by {(latency_ratio-1)*100:.1f}%",
                    root_cause_analysis="Possible resource contention or downstream service issues",
                    impact_assessment="Users experiencing slower response times",
                    affected_metrics=["response_time"],
                    baseline_values={"response_time": baseline_latency},
                    current_values={"response_time": current_latency},
                    deviation_percentage=(latency_ratio - 1) * 100,
                    detection_rules=["latency_spike_threshold"],
                    related_failures=[],
                    mitigation_suggestions=[
                        "Check resource utilization",
                        "Investigate downstream dependencies",
                        "Consider scaling resources",
                        "Review recent deployments"
                    ]
                )
        
        return None
    
    @staticmethod
    def detect_error_rate_increase(current_error_rate: float,
                                 baseline_error_rate: float,
                                 threshold: float = 0.05) -> Optional[FailureDetection]:
        """Detect increase in error rates"""
        
        error_increase = current_error_rate - baseline_error_rate
        
        if error_increase > threshold:
            severity = min(error_increase / 0.2, 1.0)  # Normalize to 0-1
            
            return FailureDetection(
                id=str(uuid.uuid4()),
                organization_id="org_demo",
                failure_type=FailureType.ERROR_RATE_INCREASE,
                detected_at=datetime.now(),
                detection_method="threshold",
                affected_component="api",
                component_id="api_001",
                severity_score=severity,
                confidence_level=0.88,
                failure_description=f"Error rate increased by {error_increase*100:.1f} percentage points",
                root_cause_analysis="Possible service instability or input validation issues",
                impact_assessment="Increased failure rate affecting user requests",
                affected_metrics=["error_rate"],
                baseline_values={"error_rate": baseline_error_rate},
                current_values={"error_rate": current_error_rate},
                deviation_percentage=error_increase * 100,
                detection_rules=["error_rate_threshold"],
                related_failures=[],
                mitigation_suggestions=[
                    "Review error logs for patterns",
                    "Check input validation logic",
                    "Investigate service dependencies",
                    "Consider circuit breaker activation"
                ]
            )
        
        return None
    
    @staticmethod
    def detect_bias_drift(current_bias_scores: Dict[str, float],
                         baseline_bias_scores: Dict[str, float],
                         threshold: float = 0.1) -> Optional[FailureDetection]:
        """Detect bias drift in model outputs"""
        
        max_drift = 0.0
        affected_categories = []
        current_values = {}
        baseline_values = {}
        
        for category, current_score in current_bias_scores.items():
            if category in baseline_bias_scores:
                baseline_score = baseline_bias_scores[category]
                drift = abs(current_score - baseline_score)
                
                if drift > threshold:
                    max_drift = max(max_drift, drift)
                    affected_categories.append(category)
                    current_values[category] = current_score
                    baseline_values[category] = baseline_score
        
        if max_drift > threshold:
            return FailureDetection(
                id=str(uuid.uuid4()),
                organization_id="org_demo",
                failure_type=FailureType.BIAS_DRIFT,
                detected_at=datetime.now(),
                detection_method="threshold",
                affected_component="model",
                component_id="model_001",
                severity_score=min(max_drift / 0.3, 1.0),
                confidence_level=0.82,
                failure_description=f"Bias drift detected in categories: {', '.join(affected_categories)}",
                root_cause_analysis="Model bias patterns have shifted from baseline",
                impact_assessment="Potential fairness issues in model outputs",
                affected_metrics=affected_categories,
                baseline_values=baseline_values,
                current_values=current_values,
                deviation_percentage=max_drift * 100,
                detection_rules=["bias_drift_threshold"],
                related_failures=[],
                mitigation_suggestions=[
                    "Review training data for bias",
                    "Implement bias correction techniques",
                    "Audit recent model changes",
                    "Consider bias-aware retraining"
                ]
            )
        
        return None


# Alert Management Engine
class AlertEngine:
    """Engine for managing alerts and notifications"""
    
    @staticmethod
    def create_alert_from_failure(failure: FailureDetection,
                                notification_channels: List[NotificationChannel] = None) -> Alert:
        """Create an alert from a detected failure"""
        
        if notification_channels is None:
            notification_channels = [NotificationChannel.EMAIL, NotificationChannel.DASHBOARD]
        
        # Determine severity based on failure severity score
        if failure.severity_score >= 0.8:
            severity = AlertSeverity.CRITICAL
        elif failure.severity_score >= 0.6:
            severity = AlertSeverity.HIGH
        elif failure.severity_score >= 0.4:
            severity = AlertSeverity.MEDIUM
        else:
            severity = AlertSeverity.LOW
        
        # Generate alert title and description
        title = f"{failure.failure_type.value.replace('_', ' ').title()} Detected"
        description = f"{failure.failure_description}\n\nAffected Component: {failure.affected_component}\nSeverity Score: {failure.severity_score:.2f}"
        
        return Alert(
            id=str(uuid.uuid4()),
            organization_id=failure.organization_id,
            alert_type="failure",
            severity=severity,
            status=AlertStatus.OPEN,
            title=title,
            description=description,
            source_failure_id=failure.id,
            source_component=failure.affected_component,
            source_metric=failure.affected_metrics[0] if failure.affected_metrics else None,
            triggered_at=failure.detected_at,
            triggered_by="system",
            acknowledgment_required=severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH],
            notification_channels=notification_channels,
            tags=[failure.failure_type.value, failure.affected_component]
        )
    
    @staticmethod
    def should_escalate_alert(alert: Alert, escalation_rules: List[Dict[str, Any]]) -> bool:
        """Determine if an alert should be escalated"""
        
        now = datetime.now()
        alert_age = (now - alert.triggered_at).total_seconds() / 60  # Minutes
        
        for rule in escalation_rules:
            if (alert.severity.value == rule.get('severity') and
                alert_age > rule.get('time_threshold_minutes', 60) and
                alert.status == AlertStatus.OPEN):
                return True
        
        return False
    
    @staticmethod
    def calculate_alert_priority(alert: Alert) -> int:
        """Calculate alert priority (1 = highest, 5 = lowest)"""
        
        base_priority = {
            AlertSeverity.CRITICAL: 1,
            AlertSeverity.HIGH: 2,
            AlertSeverity.MEDIUM: 3,
            AlertSeverity.LOW: 4,
            AlertSeverity.INFO: 5
        }
        
        priority = base_priority.get(alert.severity, 3)
        
        # Adjust based on escalation level
        priority = max(1, priority - alert.escalation_level)
        
        # Adjust based on acknowledgment status
        if alert.status == AlertStatus.OPEN and alert.acknowledgment_required:
            priority = max(1, priority - 1)
        
        return priority


# Health Monitoring Engine
class HealthMonitoringEngine:
    """Engine for monitoring overall system health"""
    
    @staticmethod
    def calculate_system_health(alerts: List[Alert],
                              incidents: List[Incident],
                              failures: List[FailureDetection],
                              performance_metrics: Dict[str, float]) -> SystemHealth:
        """Calculate overall system health score"""
        
        now = datetime.now()
        
        # Count active issues
        active_alerts = [a for a in alerts if a.status in [AlertStatus.OPEN, AlertStatus.ACKNOWLEDGED]]
        critical_alerts = [a for a in active_alerts if a.severity == AlertSeverity.CRITICAL]
        open_incidents = [i for i in incidents if i.status not in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]]
        recent_failures = [f for f in failures if (now - f.detected_at).total_seconds() < 3600]  # Last hour
        
        # Calculate health score
        health_score = 1.0
        
        # Deduct for active issues
        health_score -= len(critical_alerts) * 0.2
        health_score -= len(active_alerts) * 0.05
        health_score -= len(open_incidents) * 0.15
        health_score -= len(recent_failures) * 0.03
        
        # Adjust based on performance metrics
        if 'error_rate' in performance_metrics:
            health_score -= performance_metrics['error_rate'] * 0.5
        
        if 'response_time' in performance_metrics and performance_metrics['response_time'] > 2.0:
            health_score -= 0.1
        
        health_score = max(0.0, min(1.0, health_score))
        
        # Component health (simplified)
        component_health = {
            "models": 0.9 - len([f for f in recent_failures if f.affected_component == "model"]) * 0.1,
            "apis": 0.95 - len([f for f in recent_failures if f.affected_component == "api"]) * 0.1,
            "pipelines": 0.88 - len([f for f in recent_failures if f.affected_component == "pipeline"]) * 0.1,
            "integrations": 0.92 - len([f for f in recent_failures if f.affected_component == "integration"]) * 0.1
        }
        
        # Ensure component health is between 0 and 1
        for component in component_health:
            component_health[component] = max(0.0, min(1.0, component_health[component]))
        
        # Trend analysis (simplified)
        trend_analysis = {
            "response_time": "stable",
            "error_rate": "improving" if performance_metrics.get('error_rate', 0) < 0.01 else "stable",
            "throughput": "stable",
            "quality_score": "improving"
        }
        
        return SystemHealth(
            id=str(uuid.uuid4()),
            organization_id="org_demo",
            timestamp=now,
            overall_health_score=health_score,
            component_health=component_health,
            active_alerts_count=len(active_alerts),
            critical_alerts_count=len(critical_alerts),
            open_incidents_count=len(open_incidents),
            recent_failures_count=len(recent_failures),
            performance_metrics=performance_metrics,
            availability_percentage=99.5 - len(critical_alerts) * 0.5,
            error_rate_percentage=performance_metrics.get('error_rate', 0.005) * 100,
            mean_response_time=performance_metrics.get('response_time', 1.2),
            p95_response_time=performance_metrics.get('p95_response_time', 2.1),
            throughput_per_minute=performance_metrics.get('throughput', 150.0),
            resource_utilization={
                "cpu": 65.0,
                "memory": 72.0,
                "disk": 45.0,
                "network": 38.0
            },
            trend_analysis=trend_analysis
        )


# Notification Engine
class NotificationEngine:
    """Engine for sending notifications through various channels"""
    
    @staticmethod
    def format_alert_notification(alert: Alert, template: NotificationTemplate) -> Dict[str, str]:
        """Format alert notification using template"""
        
        # Template variables
        variables = {
            "alert_title": alert.title,
            "alert_description": alert.description,
            "severity": alert.severity.value.upper(),
            "component": alert.source_component,
            "triggered_at": alert.triggered_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "alert_id": alert.id,
            "organization": alert.organization_id
        }
        
        # Replace variables in templates
        subject = template.subject_template
        body = template.body_template
        
        for var, value in variables.items():
            subject = subject.replace(f"{{{var}}}", str(value))
            body = body.replace(f"{{{var}}}", str(value))
        
        return {
            "subject": subject,
            "body": body,
            "variables_used": variables
        }
    
    @staticmethod
    def should_suppress_notification(alert: Alert, 
                                   recent_notifications: List[Dict[str, Any]],
                                   suppression_duration: int = 60) -> bool:
        """Check if notification should be suppressed due to recent similar alerts"""
        
        now = datetime.now()
        suppression_window = now - timedelta(minutes=suppression_duration)
        
        for notification in recent_notifications:
            notification_time = datetime.fromisoformat(notification['sent_at'])
            if (notification_time > suppression_window and
                notification.get('alert_type') == alert.alert_type and
                notification.get('source_component') == alert.source_component):
                return True
        
        return False

