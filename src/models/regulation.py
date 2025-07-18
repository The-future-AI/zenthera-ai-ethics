"""
ZenThera AI Ethics Platform
Feature 2: Regulation Sync Module - Data Models

This module defines the data models for regulatory compliance tracking,
including regulations, alerts, templates, and monitoring systems.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import uuid


class Regulation:
    """
    Model for storing regulatory documents and their metadata.
    Supports AI Act, GDPR, ISO standards, NIST frameworks, etc.
    """
    
    def __init__(self, 
                 title: str,
                 regulation_type: str,
                 source: str,
                 version: str,
                 effective_date: datetime,
                 content: str,
                 url: str = None,
                 jurisdiction: str = "EU",
                 status: str = "active"):
        """
        Initialize a Regulation instance.
        
        Args:
            title: Official title of the regulation
            regulation_type: Type (ai_act, gdpr, iso_standard, nist_framework)
            source: Official source (eur_lex, iso_org, nist_gov)
            version: Version identifier
            effective_date: When the regulation becomes effective
            content: Full text content of the regulation
            url: Official URL to the regulation
            jurisdiction: Geographic scope (EU, US, Global)
            status: Current status (active, draft, superseded)
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.regulation_type = regulation_type
        self.source = source
        self.version = version
        self.effective_date = effective_date
        self.content = content
        self.url = url
        self.jurisdiction = jurisdiction
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Metadata for tracking changes
        self.change_summary = ""
        self.impact_level = "medium"  # low, medium, high, critical
        self.affected_articles = []
        self.keywords = []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert regulation to dictionary format."""
        return {
            "id": self.id,
            "title": self.title,
            "regulation_type": self.regulation_type,
            "source": self.source,
            "version": self.version,
            "effective_date": self.effective_date.isoformat(),
            "content": self.content,
            "url": self.url,
            "jurisdiction": self.jurisdiction,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "change_summary": self.change_summary,
            "impact_level": self.impact_level,
            "affected_articles": self.affected_articles,
            "keywords": self.keywords
        }


class RegulatoryAlert:
    """
    Model for regulatory change alerts and notifications.
    Tracks when regulations change and notifies relevant stakeholders.
    """
    
    def __init__(self,
                 regulation_id: str,
                 alert_type: str,
                 title: str,
                 description: str,
                 impact_level: str,
                 affected_systems: List[str] = None):
        """
        Initialize a RegulatoryAlert instance.
        
        Args:
            regulation_id: ID of the related regulation
            alert_type: Type of alert (new_regulation, amendment, deadline, clarification)
            title: Brief title of the alert
            description: Detailed description of the change
            impact_level: Impact level (low, medium, high, critical)
            affected_systems: List of systems that may be affected
        """
        self.id = str(uuid.uuid4())
        self.regulation_id = regulation_id
        self.alert_type = alert_type
        self.title = title
        self.description = description
        self.impact_level = impact_level
        self.affected_systems = affected_systems or []
        self.created_at = datetime.utcnow()
        
        # Alert management
        self.status = "active"  # active, acknowledged, resolved, dismissed
        self.priority = self._calculate_priority()
        self.deadline = None  # For deadline-based alerts
        self.action_required = True
        self.notification_sent = False
        
        # Tracking
        self.acknowledged_by = []
        self.resolved_by = None
        self.resolution_notes = ""
        
    def _calculate_priority(self) -> int:
        """Calculate alert priority based on impact level and type."""
        priority_matrix = {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4
        }
        
        type_modifier = {
            "new_regulation": 0,
            "amendment": 0,
            "deadline": -1,  # Higher priority
            "clarification": 1   # Lower priority
        }
        
        base_priority = priority_matrix.get(self.impact_level, 3)
        modifier = type_modifier.get(self.alert_type, 0)
        
        return max(1, base_priority + modifier)
    
    def acknowledge(self, user_id: str, notes: str = ""):
        """Mark alert as acknowledged by a user."""
        if user_id not in self.acknowledged_by:
            self.acknowledged_by.append(user_id)
        
        if notes:
            self.resolution_notes += f"\nAcknowledged by {user_id}: {notes}"
    
    def resolve(self, user_id: str, notes: str = ""):
        """Mark alert as resolved."""
        self.status = "resolved"
        self.resolved_by = user_id
        self.resolution_notes += f"\nResolved by {user_id}: {notes}"
        self.action_required = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary format."""
        return {
            "id": self.id,
            "regulation_id": self.regulation_id,
            "alert_type": self.alert_type,
            "title": self.title,
            "description": self.description,
            "impact_level": self.impact_level,
            "affected_systems": self.affected_systems,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "priority": self.priority,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "action_required": self.action_required,
            "notification_sent": self.notification_sent,
            "acknowledged_by": self.acknowledged_by,
            "resolved_by": self.resolved_by,
            "resolution_notes": self.resolution_notes
        }


class RegulatoryTemplate:
    """
    Model for regulatory compliance templates and checklists.
    Provides pre-built templates for common compliance scenarios.
    """
    
    def __init__(self,
                 name: str,
                 regulation_type: str,
                 template_type: str,
                 content: Dict[str, Any],
                 description: str = ""):
        """
        Initialize a RegulatoryTemplate instance.
        
        Args:
            name: Human-readable name of the template
            regulation_type: Related regulation (ai_act, gdpr, iso_27001, etc.)
            template_type: Type of template (checklist, assessment, report, policy)
            content: Template content structure
            description: Description of the template's purpose
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.regulation_type = regulation_type
        self.template_type = template_type
        self.content = content
        self.description = description
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Template metadata
        self.version = "1.0"
        self.author = "ZenThera AI Ethics Platform"
        self.tags = []
        self.usage_count = 0
        self.is_active = True
        
        # Validation rules
        self.required_fields = []
        self.validation_rules = {}
        
    def validate_content(self, user_content: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user-provided content against template rules."""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "completion_percentage": 0
        }
        
        # Check required fields
        missing_fields = []
        for field in self.required_fields:
            if field not in user_content or not user_content[field]:
                missing_fields.append(field)
        
        if missing_fields:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Calculate completion percentage
        total_fields = len(self.content.get("fields", []))
        completed_fields = len([f for f in user_content.keys() if user_content[f]])
        
        if total_fields > 0:
            validation_result["completion_percentage"] = (completed_fields / total_fields) * 100
        
        return validation_result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "regulation_type": self.regulation_type,
            "template_type": self.template_type,
            "content": self.content,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
            "usage_count": self.usage_count,
            "is_active": self.is_active,
            "required_fields": self.required_fields,
            "validation_rules": self.validation_rules
        }


class RegulationMonitor:
    """
    Model for tracking regulation monitoring configurations.
    Defines what regulations to monitor and how to process changes.
    """
    
    def __init__(self,
                 name: str,
                 regulation_types: List[str],
                 sources: List[str],
                 keywords: List[str],
                 organization_id: str):
        """
        Initialize a RegulationMonitor instance.
        
        Args:
            name: Name of the monitoring configuration
            regulation_types: Types of regulations to monitor
            sources: Sources to monitor (eur_lex, iso_org, nist_gov)
            keywords: Keywords to watch for in changes
            organization_id: ID of the organization this monitor belongs to
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.regulation_types = regulation_types
        self.sources = sources
        self.keywords = keywords
        self.organization_id = organization_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Monitoring configuration
        self.is_active = True
        self.check_frequency = "daily"  # hourly, daily, weekly
        self.last_check = None
        self.next_check = None
        
        # Notification settings
        self.notification_channels = ["email"]  # email, slack, teams, webhook
        self.notification_threshold = "medium"  # low, medium, high, critical
        self.recipients = []
        
        # Statistics
        self.total_checks = 0
        self.alerts_generated = 0
        self.last_alert_date = None
        
    def should_generate_alert(self, impact_level: str) -> bool:
        """Determine if an alert should be generated based on threshold."""
        impact_levels = ["low", "medium", "high", "critical"]
        threshold_index = impact_levels.index(self.notification_threshold)
        impact_index = impact_levels.index(impact_level)
        
        return impact_index >= threshold_index
    
    def update_statistics(self, alerts_count: int = 0):
        """Update monitoring statistics."""
        self.total_checks += 1
        self.last_check = datetime.utcnow()
        
        if alerts_count > 0:
            self.alerts_generated += alerts_count
            self.last_alert_date = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert monitor to dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "regulation_types": self.regulation_types,
            "sources": self.sources,
            "keywords": self.keywords,
            "organization_id": self.organization_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "check_frequency": self.check_frequency,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "next_check": self.next_check.isoformat() if self.next_check else None,
            "notification_channels": self.notification_channels,
            "notification_threshold": self.notification_threshold,
            "recipients": self.recipients,
            "total_checks": self.total_checks,
            "alerts_generated": self.alerts_generated,
            "last_alert_date": self.last_alert_date.isoformat() if self.last_alert_date else None
        }


# Sample data for testing and demonstration
def create_sample_regulations():
    """Create sample regulation data for testing."""
    
    # AI Act sample
    ai_act = Regulation(
        title="Regulation (EU) 2024/1689 - Artificial Intelligence Act",
        regulation_type="ai_act",
        source="eur_lex",
        version="2024.1",
        effective_date=datetime(2026, 8, 2),
        content="The AI Act establishes harmonized rules for artificial intelligence...",
        url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        jurisdiction="EU",
        status="active"
    )
    ai_act.keywords = ["artificial intelligence", "high-risk AI", "prohibited practices", "transparency"]
    ai_act.impact_level = "critical"
    
    # GDPR sample
    gdpr = Regulation(
        title="General Data Protection Regulation (GDPR)",
        regulation_type="gdpr",
        source="eur_lex",
        version="2016.679",
        effective_date=datetime(2018, 5, 25),
        content="This Regulation lays down rules relating to the protection of natural persons...",
        url="https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        jurisdiction="EU",
        status="active"
    )
    gdpr.keywords = ["personal data", "data protection", "consent", "privacy"]
    gdpr.impact_level = "high"
    
    return [ai_act, gdpr]


def create_sample_templates():
    """Create sample regulatory templates."""
    
    # AI Act Risk Assessment Template
    ai_act_template = RegulatoryTemplate(
        name="AI Act High-Risk System Assessment",
        regulation_type="ai_act",
        template_type="assessment",
        content={
            "sections": [
                {
                    "title": "System Classification",
                    "fields": [
                        {"name": "system_name", "type": "text", "required": True},
                        {"name": "intended_purpose", "type": "textarea", "required": True},
                        {"name": "risk_category", "type": "select", "options": ["High-risk", "Limited risk", "Minimal risk"]},
                        {"name": "prohibited_practices", "type": "checkbox", "required": True}
                    ]
                },
                {
                    "title": "Technical Documentation",
                    "fields": [
                        {"name": "training_data", "type": "textarea", "required": True},
                        {"name": "model_architecture", "type": "textarea", "required": True},
                        {"name": "performance_metrics", "type": "textarea", "required": True}
                    ]
                },
                {
                    "title": "Risk Management",
                    "fields": [
                        {"name": "risk_assessment", "type": "textarea", "required": True},
                        {"name": "mitigation_measures", "type": "textarea", "required": True},
                        {"name": "monitoring_plan", "type": "textarea", "required": True}
                    ]
                }
            ]
        },
        description="Comprehensive assessment template for AI systems under the EU AI Act"
    )
    ai_act_template.required_fields = ["system_name", "intended_purpose", "prohibited_practices", "training_data", "risk_assessment"]
    ai_act_template.tags = ["ai_act", "risk_assessment", "high_risk", "compliance"]
    
    return [ai_act_template]

