"""
ZenThera AI Ethics Platform
Feature 4: Narrative Explainability & Replay - API Routes

This module provides comprehensive APIs for session replay, narrative explanations,
ethical alignment assessment, and audit trail management.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
import json
from models.narrative_explainability import (
    SessionReplay, ReplayEvent, NarrativeExplanation, EthicalAlignment,
    AuditTrail, ExplanationTemplate, NarrativeGenerator, EthicalAlignmentEngine,
    ExplanationType, AlignmentCategory, ReplayEventType, NarrativeStyle
)

narrative_explainability_bp = Blueprint('narrative_explainability', __name__)

# In-memory storage for demo (would be replaced with actual database)
session_replays_db = {}
replay_events_db = {}
narrative_explanations_db = {}
ethical_alignments_db = {}
audit_trails_db = {}
explanation_templates_db = {}

# Initialize with sample data
def initialize_sample_data():
    """Initialize with realistic sample data for demonstration"""
    
    # Sample session replay
    replay1 = SessionReplay(
        id="replay_001",
        session_id="session_001",
        organization_id="org_demo",
        created_at=datetime.now() - timedelta(hours=1),
        created_by="user_001",
        replay_name="Customer Support Session - Privacy Concern",
        description="Session involving potential privacy leak detection and resolution",
        session_start=datetime.now() - timedelta(hours=2),
        session_end=datetime.now() - timedelta(hours=1, minutes=30),
        total_events=8,
        total_duration_seconds=1800,
        participants=["user_001", "system"],
        models_used=["gpt-4"],
        tags=["privacy", "customer-support", "high-risk"]
    )
    session_replays_db[replay1.id] = replay1
    
    # Sample replay events
    events_data = [
        {
            "event_type": ReplayEventType.USER_INPUT,
            "actor_type": "user",
            "event_data": {
                "prompt": "What's my account balance?",
                "user_context": "Customer inquiry"
            }
        },
        {
            "event_type": ReplayEventType.MODEL_RESPONSE,
            "actor_type": "model",
            "event_data": {
                "response": "Your account balance is $2,450.67. Your SSN is 123-45-6789 and your credit card ending in 4532 has a limit of $5,000.",
                "model_name": "gpt-4",
                "latency_ms": 1500
            }
        },
        {
            "event_type": ReplayEventType.RISK_DETECTION,
            "actor_type": "system",
            "event_data": {
                "risk_type": "privacy_leak",
                "risk_score": 0.95,
                "detected_pii": ["ssn", "credit_card"]
            }
        },
        {
            "event_type": ReplayEventType.SYSTEM_INTERVENTION,
            "actor_type": "system",
            "event_data": {
                "action": "response_blocked",
                "reason": "Privacy violation detected",
                "alternative_response": "I can help you with your account balance, but I cannot display sensitive information here. Please log into your secure account portal."
            }
        },
        {
            "event_type": ReplayEventType.HUMAN_REVIEW,
            "actor_type": "human_reviewer",
            "event_data": {
                "reviewer_id": "reviewer_001",
                "review_decision": "confirmed_violation",
                "notes": "Clear privacy leak - SSN and credit card info exposed"
            }
        }
    ]
    
    for i, event_data in enumerate(events_data):
        event = ReplayEvent(
            id=f"event_{i+1:03d}",
            replay_id=replay1.id,
            session_id=replay1.session_id,
            organization_id="org_demo",
            event_type=event_data["event_type"],
            timestamp=replay1.session_start + timedelta(minutes=i*5),
            sequence_number=i+1,
            event_data=event_data["event_data"],
            actor_id=f"actor_{i+1}",
            actor_type=event_data["actor_type"],
            duration_ms=2000 + i*500,
            related_interaction_id=f"interaction_{i+1:03d}" if i < 2 else None
        )
        replay_events_db[event.id] = event
    
    # Sample narrative explanations
    explanation1 = NarrativeExplanation(
        id="explanation_001",
        organization_id="org_demo",
        explanation_type=ExplanationType.RISK_EXPLANATION,
        target_entity_id="risk_004",
        target_entity_type="risk",
        narrative_style=NarrativeStyle.EXECUTIVE,
        title="Privacy Leak Detection: Executive Summary",
        summary="Critical privacy violation detected and prevented in customer support interaction",
        detailed_explanation=NarrativeGenerator.generate_risk_explanation({
            "risk_type": "privacy_leak",
            "risk_score": 0.95,
            "confidence": 0.98,
            "evidence": {"ssn_found": 1, "credit_card_found": 1}
        }, NarrativeStyle.EXECUTIVE),
        key_factors=["SSN exposure", "Credit card information leak", "Automated detection", "System intervention"],
        evidence_points=[
            {"type": "ssn_detection", "value": "123-45-6789", "confidence": 0.99},
            {"type": "credit_card", "value": "ending in 4532", "confidence": 0.95}
        ],
        confidence_level=0.98,
        generated_at=datetime.now() - timedelta(minutes=30),
        generated_by="system",
        generation_method="automated",
        is_approved=True
    )
    narrative_explanations_db[explanation1.id] = explanation1
    
    # Sample ethical alignment
    alignment1 = EthicalAlignment(
        id="alignment_001",
        organization_id="org_demo",
        target_entity_id="interaction_004",
        target_entity_type="interaction",
        assessment_timestamp=datetime.now() - timedelta(minutes=25),
        assessor_id="system",
        overall_alignment_score=0.23,  # Low due to privacy violation
        category_scores={
            AlignmentCategory.BENEFICENCE: 0.6,
            AlignmentCategory.NON_MALEFICENCE: 0.1,  # Very low due to harm
            AlignmentCategory.AUTONOMY: 0.7,
            AlignmentCategory.JUSTICE: 0.5,
            AlignmentCategory.TRANSPARENCY: 0.3,
            AlignmentCategory.ACCOUNTABILITY: 0.2,
            AlignmentCategory.PRIVACY: 0.0,  # Zero due to privacy leak
            AlignmentCategory.HUMAN_DIGNITY: 0.4
        },
        alignment_analysis="Severe privacy violation detected. While the response attempted to be helpful (beneficence), it caused significant harm by exposing sensitive personal information.",
        strengths=["Attempted to provide helpful information", "Quick response time"],
        concerns=["Exposed SSN and credit card information", "No privacy safeguards", "Potential regulatory violation"],
        recommendations=["Implement PII detection before response", "Add privacy filters", "Review data handling procedures"],
        compliance_notes="GDPR Article 32 violation - inadequate security measures",
        requires_human_review=True,
        review_priority="critical"
    )
    ethical_alignments_db[alignment1.id] = alignment1
    
    # Sample audit trail
    audit1 = AuditTrail(
        id="audit_001",
        organization_id="org_demo",
        audit_type="privacy_incident",
        target_entity_id="session_001",
        target_entity_type="session",
        audit_timestamp=datetime.now() - timedelta(minutes=15),
        auditor_id="auditor_001",
        audit_scope=["privacy_compliance", "data_protection", "system_response"],
        findings=[
            {
                "finding_id": "F001",
                "category": "privacy_violation",
                "severity": "critical",
                "description": "SSN and credit card information exposed in model response",
                "evidence": "Response contained 123-45-6789 (SSN) and credit card ending in 4532"
            },
            {
                "finding_id": "F002", 
                "category": "system_response",
                "severity": "high",
                "description": "Automated detection and intervention successful",
                "evidence": "System detected privacy leak with 95% confidence and blocked response"
            }
        ],
        compliance_status="non_compliant",
        risk_level="critical",
        recommendations=[
            "Implement pre-response PII scanning",
            "Update model training to avoid PII generation",
            "Enhance privacy safeguards",
            "Conduct staff training on privacy protocols"
        ],
        action_items=[
            {
                "item_id": "A001",
                "description": "Deploy PII detection filter",
                "assigned_to": "tech_team",
                "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
                "priority": "critical"
            },
            {
                "item_id": "A002",
                "description": "Review and update privacy policies",
                "assigned_to": "compliance_team", 
                "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "priority": "high"
            }
        ],
        follow_up_required=True,
        follow_up_date=datetime.now() + timedelta(days=7),
        audit_report="Critical privacy incident requiring immediate remediation and process improvements."
    )
    audit_trails_db[audit1.id] = audit1

# Initialize sample data
initialize_sample_data()


@narrative_explainability_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get narrative explainability dashboard data"""
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
        org_replays = [r for r in session_replays_db.values() if r.organization_id == org_id]
        org_explanations = [e for e in narrative_explanations_db.values() 
                          if e.organization_id == org_id and e.generated_at >= start_time]
        org_alignments = [a for a in ethical_alignments_db.values() 
                         if a.organization_id == org_id and a.assessment_timestamp >= start_time]
        org_audits = [a for a in audit_trails_db.values() 
                     if a.organization_id == org_id and a.audit_timestamp >= start_time]
        
        # Calculate metrics
        total_replays = len(org_replays)
        total_explanations = len(org_explanations)
        total_alignments = len(org_alignments)
        total_audits = len(org_audits)
        
        # Ethical alignment metrics
        avg_alignment_score = sum(a.overall_alignment_score for a in org_alignments) / len(org_alignments) if org_alignments else 0
        high_risk_alignments = len([a for a in org_alignments if a.overall_alignment_score < 0.5])
        
        # Explanation type distribution
        explanation_types = {}
        for explanation in org_explanations:
            exp_type = explanation.explanation_type.value
            if exp_type not in explanation_types:
                explanation_types[exp_type] = 0
            explanation_types[exp_type] += 1
        
        # Audit findings
        critical_findings = len([a for a in org_audits if a.risk_level == "critical"])
        pending_actions = sum(len([item for item in audit.action_items if item.get('status', 'pending') == 'pending']) 
                            for audit in org_audits)
        
        return jsonify({
            "status": "success",
            "data": {
                "overview": {
                    "total_session_replays": total_replays,
                    "total_explanations_generated": total_explanations,
                    "total_ethical_assessments": total_alignments,
                    "total_audit_trails": total_audits,
                    "average_ethical_alignment": round(avg_alignment_score, 3),
                    "high_risk_interactions": high_risk_alignments,
                    "critical_audit_findings": critical_findings,
                    "pending_action_items": pending_actions
                },
                "explanation_types": explanation_types,
                "recent_replays": [r.to_dict() for r in sorted(org_replays, key=lambda x: x.created_at, reverse=True)[:5]],
                "recent_alignments": [a.to_dict() for a in sorted(org_alignments, key=lambda x: x.assessment_timestamp, reverse=True)[:5]],
                "time_range": time_range,
                "last_updated": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/replays', methods=['GET'])
def get_session_replays():
    """Get list of session replays with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        session_id = request.args.get('session_id')
        tags = request.args.get('tags', '').split(',') if request.args.get('tags') else []
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Filter replays
        filtered_replays = []
        for replay in session_replays_db.values():
            if replay.organization_id != org_id:
                continue
            if session_id and replay.session_id != session_id:
                continue
            if tags and not any(tag in replay.tags for tag in tags):
                continue
            
            filtered_replays.append(replay)
        
        # Sort by creation time (newest first)
        filtered_replays.sort(key=lambda x: x.created_at, reverse=True)
        
        # Apply pagination
        total_count = len(filtered_replays)
        paginated_replays = filtered_replays[offset:offset + limit]
        
        # Enrich with event counts and metadata
        enriched_replays = []
        for replay in paginated_replays:
            replay_dict = replay.to_dict()
            
            # Add event information
            replay_events = [e for e in replay_events_db.values() if e.replay_id == replay.id]
            replay_dict['event_count'] = len(replay_events)
            replay_dict['event_types'] = list(set(e.event_type.value for e in replay_events))
            
            # Add related explanations
            related_explanations = [e for e in narrative_explanations_db.values() 
                                  if e.target_entity_id == replay.session_id]
            replay_dict['explanation_count'] = len(related_explanations)
            
            enriched_replays.append(replay_dict)
        
        return jsonify({
            "status": "success",
            "data": {
                "replays": enriched_replays,
                "pagination": {
                    "total_count": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/replays', methods=['POST'])
def create_session_replay():
    """Create a new session replay"""
    try:
        data = request.get_json()
        
        replay = SessionReplay(
            id=str(uuid.uuid4()),
            session_id=data['session_id'],
            organization_id=data['organization_id'],
            created_at=datetime.now(),
            created_by=data['created_by'],
            replay_name=data['replay_name'],
            description=data.get('description', ''),
            session_start=datetime.fromisoformat(data['session_start']),
            session_end=datetime.fromisoformat(data['session_end']),
            total_events=data.get('total_events', 0),
            total_duration_seconds=data.get('total_duration_seconds', 0),
            participants=data.get('participants', []),
            models_used=data.get('models_used', []),
            tags=data.get('tags', [])
        )
        
        session_replays_db[replay.id] = replay
        
        return jsonify({
            "status": "success",
            "data": {
                "replay": replay.to_dict(),
                "message": "Session replay created successfully"
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/replays/<replay_id>/events', methods=['GET'])
def get_replay_events(replay_id):
    """Get events for a specific replay"""
    try:
        if replay_id not in session_replays_db:
            return jsonify({"status": "error", "message": "Replay not found"}), 404
        
        # Get all events for this replay
        replay_events = [e for e in replay_events_db.values() if e.replay_id == replay_id]
        replay_events.sort(key=lambda x: x.sequence_number)
        
        # Enrich events with additional context
        enriched_events = []
        for event in replay_events:
            event_dict = event.to_dict()
            
            # Add timing information
            if len(enriched_events) > 0:
                prev_event = enriched_events[-1]
                time_diff = (event.timestamp - datetime.fromisoformat(prev_event['timestamp'])).total_seconds()
                event_dict['time_since_previous'] = time_diff
            else:
                event_dict['time_since_previous'] = 0
            
            enriched_events.append(event_dict)
        
        return jsonify({
            "status": "success",
            "data": {
                "replay_id": replay_id,
                "events": enriched_events,
                "total_events": len(enriched_events),
                "event_types": list(set(e.event_type.value for e in replay_events))
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/explanations', methods=['GET'])
def get_explanations():
    """Get narrative explanations with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        explanation_type = request.args.get('explanation_type')
        narrative_style = request.args.get('narrative_style')
        target_entity_id = request.args.get('target_entity_id')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Filter explanations
        filtered_explanations = []
        for explanation in narrative_explanations_db.values():
            if explanation.organization_id != org_id:
                continue
            if explanation_type and explanation.explanation_type.value != explanation_type:
                continue
            if narrative_style and explanation.narrative_style.value != narrative_style:
                continue
            if target_entity_id and explanation.target_entity_id != target_entity_id:
                continue
            
            filtered_explanations.append(explanation)
        
        # Sort by generation time (newest first)
        filtered_explanations.sort(key=lambda x: x.generated_at, reverse=True)
        
        # Apply pagination
        total_count = len(filtered_explanations)
        paginated_explanations = filtered_explanations[offset:offset + limit]
        
        return jsonify({
            "status": "success",
            "data": {
                "explanations": [e.to_dict() for e in paginated_explanations],
                "pagination": {
                    "total_count": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "summary": {
                    "total_explanations": total_count,
                    "by_type": {
                        exp_type.value: len([e for e in filtered_explanations if e.explanation_type == exp_type])
                        for exp_type in ExplanationType
                    },
                    "by_style": {
                        style.value: len([e for e in filtered_explanations if e.narrative_style == style])
                        for style in NarrativeStyle
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/explanations', methods=['POST'])
def generate_explanation():
    """Generate a new narrative explanation"""
    try:
        data = request.get_json()
        
        explanation_type = ExplanationType(data['explanation_type'])
        narrative_style = NarrativeStyle(data['narrative_style'])
        target_entity_data = data.get('target_entity_data', {})
        
        # Generate explanation based on type
        if explanation_type == ExplanationType.DECISION_RATIONALE:
            detailed_explanation = NarrativeGenerator.generate_decision_explanation(
                target_entity_data, narrative_style
            )
            title = f"Decision Analysis: {target_entity_data.get('model_name', 'AI Model')}"
            summary = "Analysis of AI decision-making process and rationale"
            key_factors = ["Input analysis", "Knowledge retrieval", "Response generation", "Quality assurance"]
            
        elif explanation_type == ExplanationType.RISK_EXPLANATION:
            detailed_explanation = NarrativeGenerator.generate_risk_explanation(
                target_entity_data, narrative_style
            )
            risk_type = target_entity_data.get('risk_type', 'Unknown')
            title = f"Risk Analysis: {risk_type.title()}"
            summary = f"Detailed explanation of {risk_type} risk detection and implications"
            key_factors = ["Risk detection", "Evidence analysis", "Severity assessment", "Mitigation recommendations"]
            
        elif explanation_type == ExplanationType.ETHICAL_ANALYSIS:
            detailed_explanation = NarrativeGenerator.generate_ethical_analysis(
                target_entity_data, narrative_style
            )
            title = "Ethical Alignment Assessment"
            summary = "Comprehensive ethical evaluation of AI interaction"
            key_factors = ["Ethical principles", "Alignment scoring", "Strengths identification", "Improvement areas"]
            
        else:
            # Generic explanation
            detailed_explanation = f"Explanation for {explanation_type.value} generated in {narrative_style.value} style."
            title = f"{explanation_type.value.replace('_', ' ').title()}"
            summary = f"Generated explanation for {explanation_type.value}"
            key_factors = ["Analysis", "Assessment", "Recommendations"]
        
        # Create explanation record
        explanation = NarrativeExplanation(
            id=str(uuid.uuid4()),
            organization_id=data['organization_id'],
            explanation_type=explanation_type,
            target_entity_id=data['target_entity_id'],
            target_entity_type=data['target_entity_type'],
            narrative_style=narrative_style,
            title=title,
            summary=summary,
            detailed_explanation=detailed_explanation,
            key_factors=key_factors,
            evidence_points=data.get('evidence_points', []),
            confidence_level=data.get('confidence_level', 0.8),
            generated_at=datetime.now(),
            generated_by=data.get('generated_by', 'system'),
            generation_method=data.get('generation_method', 'automated')
        )
        
        narrative_explanations_db[explanation.id] = explanation
        
        return jsonify({
            "status": "success",
            "data": {
                "explanation": explanation.to_dict(),
                "message": "Narrative explanation generated successfully"
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/ethical-alignment', methods=['GET'])
def get_ethical_alignments():
    """Get ethical alignment assessments"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        target_entity_id = request.args.get('target_entity_id')
        min_score = float(request.args.get('min_score', 0.0))
        max_score = float(request.args.get('max_score', 1.0))
        limit = int(request.args.get('limit', 50))
        
        # Filter alignments
        filtered_alignments = []
        for alignment in ethical_alignments_db.values():
            if alignment.organization_id != org_id:
                continue
            if target_entity_id and alignment.target_entity_id != target_entity_id:
                continue
            if not (min_score <= alignment.overall_alignment_score <= max_score):
                continue
            
            filtered_alignments.append(alignment)
        
        # Sort by assessment time (newest first)
        filtered_alignments.sort(key=lambda x: x.assessment_timestamp, reverse=True)
        
        # Apply limit
        limited_alignments = filtered_alignments[:limit]
        
        # Calculate summary statistics
        if filtered_alignments:
            avg_score = sum(a.overall_alignment_score for a in filtered_alignments) / len(filtered_alignments)
            category_averages = {}
            for category in AlignmentCategory:
                scores = [a.category_scores.get(category, 0.0) for a in filtered_alignments]
                category_averages[category.value] = sum(scores) / len(scores) if scores else 0.0
        else:
            avg_score = 0.0
            category_averages = {}
        
        return jsonify({
            "status": "success",
            "data": {
                "alignments": [a.to_dict() for a in limited_alignments],
                "summary": {
                    "total_assessments": len(filtered_alignments),
                    "average_alignment_score": round(avg_score, 3),
                    "category_averages": category_averages,
                    "high_risk_count": len([a for a in filtered_alignments if a.overall_alignment_score < 0.5]),
                    "requires_review_count": len([a for a in filtered_alignments if a.requires_human_review])
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/ethical-alignment', methods=['POST'])
def assess_ethical_alignment():
    """Perform ethical alignment assessment"""
    try:
        data = request.get_json()
        
        target_entity_data = data.get('target_entity_data', {})
        
        # Perform ethical assessment using the engine
        category_scores = {
            AlignmentCategory.BENEFICENCE: EthicalAlignmentEngine.assess_beneficence(target_entity_data),
            AlignmentCategory.NON_MALEFICENCE: EthicalAlignmentEngine.assess_non_maleficence(target_entity_data),
            AlignmentCategory.AUTONOMY: EthicalAlignmentEngine.assess_autonomy(target_entity_data),
            AlignmentCategory.JUSTICE: EthicalAlignmentEngine.assess_justice(target_entity_data),
            AlignmentCategory.TRANSPARENCY: EthicalAlignmentEngine.assess_transparency(target_entity_data),
            AlignmentCategory.ACCOUNTABILITY: EthicalAlignmentEngine.assess_accountability(target_entity_data),
            AlignmentCategory.PRIVACY: EthicalAlignmentEngine.assess_privacy(target_entity_data),
            AlignmentCategory.HUMAN_DIGNITY: EthicalAlignmentEngine.assess_human_dignity(target_entity_data)
        }
        
        # Calculate overall score
        overall_score = sum(category_scores.values()) / len(category_scores)
        
        # Determine strengths and concerns
        strengths = []
        concerns = []
        recommendations = []
        
        for category, score in category_scores.items():
            if score >= 0.8:
                strengths.append(f"Strong {category.value.replace('_', ' ')} alignment")
            elif score < 0.5:
                concerns.append(f"Low {category.value.replace('_', ' ')} score ({score:.2f})")
                recommendations.append(f"Improve {category.value.replace('_', ' ')} practices")
        
        # Generate analysis
        if overall_score >= 0.8:
            analysis = "Excellent ethical alignment across most categories. Minor improvements may be beneficial."
        elif overall_score >= 0.6:
            analysis = "Good ethical alignment with some areas for improvement identified."
        elif overall_score >= 0.4:
            analysis = "Moderate ethical alignment. Several areas require attention and improvement."
        else:
            analysis = "Poor ethical alignment. Significant improvements needed across multiple categories."
        
        # Determine review requirements
        requires_review = overall_score < 0.6 or any(score < 0.3 for score in category_scores.values())
        if overall_score < 0.3:
            review_priority = "critical"
        elif overall_score < 0.5:
            review_priority = "high"
        elif overall_score < 0.7:
            review_priority = "medium"
        else:
            review_priority = "low"
        
        # Create alignment record
        alignment = EthicalAlignment(
            id=str(uuid.uuid4()),
            organization_id=data['organization_id'],
            target_entity_id=data['target_entity_id'],
            target_entity_type=data['target_entity_type'],
            assessment_timestamp=datetime.now(),
            assessor_id=data.get('assessor_id', 'system'),
            overall_alignment_score=overall_score,
            category_scores=category_scores,
            alignment_analysis=analysis,
            strengths=strengths,
            concerns=concerns,
            recommendations=recommendations,
            compliance_notes=data.get('compliance_notes', ''),
            requires_human_review=requires_review,
            review_priority=review_priority
        )
        
        ethical_alignments_db[alignment.id] = alignment
        
        return jsonify({
            "status": "success",
            "data": {
                "alignment": alignment.to_dict(),
                "assessment_summary": {
                    "overall_score": round(overall_score, 3),
                    "highest_category": max(category_scores.keys(), key=lambda k: category_scores[k]).value,
                    "lowest_category": min(category_scores.keys(), key=lambda k: category_scores[k]).value,
                    "requires_review": requires_review,
                    "review_priority": review_priority
                },
                "message": "Ethical alignment assessment completed"
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/audit-trails', methods=['GET'])
def get_audit_trails():
    """Get audit trails with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        audit_type = request.args.get('audit_type')
        compliance_status = request.args.get('compliance_status')
        risk_level = request.args.get('risk_level')
        limit = int(request.args.get('limit', 50))
        
        # Filter audit trails
        filtered_audits = []
        for audit in audit_trails_db.values():
            if audit.organization_id != org_id:
                continue
            if audit_type and audit.audit_type != audit_type:
                continue
            if compliance_status and audit.compliance_status != compliance_status:
                continue
            if risk_level and audit.risk_level != risk_level:
                continue
            
            filtered_audits.append(audit)
        
        # Sort by audit time (newest first)
        filtered_audits.sort(key=lambda x: x.audit_timestamp, reverse=True)
        
        # Apply limit
        limited_audits = filtered_audits[:limit]
        
        return jsonify({
            "status": "success",
            "data": {
                "audit_trails": [a.to_dict() for a in limited_audits],
                "summary": {
                    "total_audits": len(filtered_audits),
                    "by_status": {
                        "compliant": len([a for a in filtered_audits if a.compliance_status == "compliant"]),
                        "non_compliant": len([a for a in filtered_audits if a.compliance_status == "non_compliant"]),
                        "needs_review": len([a for a in filtered_audits if a.compliance_status == "needs_review"])
                    },
                    "by_risk_level": {
                        "critical": len([a for a in filtered_audits if a.risk_level == "critical"]),
                        "high": len([a for a in filtered_audits if a.risk_level == "high"]),
                        "medium": len([a for a in filtered_audits if a.risk_level == "medium"]),
                        "low": len([a for a in filtered_audits if a.risk_level == "low"])
                    },
                    "pending_follow_ups": len([a for a in filtered_audits if a.follow_up_required])
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/audit-trails', methods=['POST'])
def create_audit_trail():
    """Create a new audit trail"""
    try:
        data = request.get_json()
        
        audit = AuditTrail(
            id=str(uuid.uuid4()),
            organization_id=data['organization_id'],
            audit_type=data['audit_type'],
            target_entity_id=data['target_entity_id'],
            target_entity_type=data['target_entity_type'],
            audit_timestamp=datetime.now(),
            auditor_id=data['auditor_id'],
            audit_scope=data['audit_scope'],
            findings=data['findings'],
            compliance_status=data['compliance_status'],
            risk_level=data['risk_level'],
            recommendations=data.get('recommendations', []),
            action_items=data.get('action_items', []),
            follow_up_required=data.get('follow_up_required', False),
            follow_up_date=datetime.fromisoformat(data['follow_up_date']) if data.get('follow_up_date') else None,
            audit_report=data.get('audit_report', ''),
            supporting_documents=data.get('supporting_documents', [])
        )
        
        audit_trails_db[audit.id] = audit
        
        return jsonify({
            "status": "success",
            "data": {
                "audit_trail": audit.to_dict(),
                "message": "Audit trail created successfully"
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/templates', methods=['GET'])
def get_explanation_templates():
    """Get explanation templates"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        explanation_type = request.args.get('explanation_type')
        narrative_style = request.args.get('narrative_style')
        
        # Filter templates
        filtered_templates = []
        for template in explanation_templates_db.values():
            if template.organization_id != org_id:
                continue
            if explanation_type and template.explanation_type.value != explanation_type:
                continue
            if narrative_style and template.narrative_style.value != narrative_style:
                continue
            if not template.is_active:
                continue
            
            filtered_templates.append(template)
        
        # Sort by usage count (most used first)
        filtered_templates.sort(key=lambda x: x.usage_count, reverse=True)
        
        return jsonify({
            "status": "success",
            "data": {
                "templates": [t.to_dict() for t in filtered_templates],
                "summary": {
                    "total_templates": len(filtered_templates),
                    "by_type": {
                        exp_type.value: len([t for t in filtered_templates if t.explanation_type == exp_type])
                        for exp_type in ExplanationType
                    },
                    "by_style": {
                        style.value: len([t for t in filtered_templates if t.narrative_style == style])
                        for style in NarrativeStyle
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@narrative_explainability_bp.route('/replay/<replay_id>/export', methods=['GET'])
def export_replay(replay_id):
    """Export session replay data"""
    try:
        if replay_id not in session_replays_db:
            return jsonify({"status": "error", "message": "Replay not found"}), 404
        
        replay = session_replays_db[replay_id]
        events = [e for e in replay_events_db.values() if e.replay_id == replay_id]
        events.sort(key=lambda x: x.sequence_number)
        
        export_data = {
            "replay_metadata": replay.to_dict(),
            "events": [e.to_dict() for e in events],
            "export_timestamp": datetime.now().isoformat(),
            "export_format": "zenthera_replay_v1.0"
        }
        
        return jsonify({
            "status": "success",
            "data": export_data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

