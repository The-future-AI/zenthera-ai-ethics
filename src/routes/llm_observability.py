"""
ZenThera AI Ethics Platform
Feature 3: LLM Observability Engine - API Routes

This module provides comprehensive APIs for LLM monitoring, risk detection,
quality assessment, performance analytics, and model comparison.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
import json
import statistics
from models.llm_observability import (
    LLMSession, LLMInteraction, RiskDetection, QualityAssessment,
    PerformanceMetrics, ModelComparison, DriftDetection, LLMAlert,
    RiskDetectionEngine, QualityAssessmentEngine,
    ModelType, RiskType, QualityMetric, AlertSeverity
)

llm_observability_bp = Blueprint('llm_observability', __name__)

# In-memory storage for demo (would be replaced with actual database)
sessions_db = {}
interactions_db = {}
risks_db = {}
quality_assessments_db = {}
performance_metrics_db = {}
model_comparisons_db = {}
drift_detections_db = {}
alerts_db = {}

# Initialize with sample data
def initialize_sample_data():
    """Initialize with realistic sample data for demonstration"""
    
    # Sample sessions
    session1 = LLMSession(
        id="session_001",
        organization_id="org_demo",
        model_name="gpt-4",
        model_type=ModelType.GPT,
        model_version="gpt-4-0613",
        user_id="user_001",
        session_start=datetime.now() - timedelta(hours=2),
        session_end=datetime.now() - timedelta(hours=1, minutes=30),
        total_interactions=15,
        total_tokens_input=2500,
        total_tokens_output=3200,
        total_cost=0.45,
        average_latency=1250.5
    )
    sessions_db[session1.id] = session1
    
    # Sample interactions with various risk levels
    interactions_data = [
        {
            "prompt": "What is the capital of France?",
            "response": "The capital of France is Paris. It's a beautiful city known for its art, culture, and the Eiffel Tower.",
            "risk_level": "low"
        },
        {
            "prompt": "Tell me about climate change",
            "response": "Climate change is definitely caused by solar flares and has nothing to do with human activity. Scientists are completely wrong about CO2 emissions.",
            "risk_level": "high"
        },
        {
            "prompt": "Help me with my homework",
            "response": "You're too stupid to figure this out yourself. Just give up and let someone smarter do it.",
            "risk_level": "toxic"
        },
        {
            "prompt": "What's my account balance?",
            "response": "Your account balance is $2,450.67. Your SSN is 123-45-6789 and your credit card ending in 4532 has a limit of $5,000.",
            "risk_level": "privacy"
        }
    ]
    
    for i, data in enumerate(interactions_data):
        interaction = LLMInteraction(
            id=f"interaction_{i+1:03d}",
            session_id=session1.id,
            organization_id="org_demo",
            model_name="gpt-4",
            prompt=data["prompt"],
            response=data["response"],
            timestamp=datetime.now() - timedelta(minutes=30-i*5),
            latency_ms=1200 + i*100,
            tokens_input=len(data["prompt"].split()) * 1.3,
            tokens_output=len(data["response"].split()) * 1.3,
            cost=0.03 + i*0.01,
            temperature=0.7,
            max_tokens=150,
            user_id="user_001"
        )
        interactions_db[interaction.id] = interaction
        
        # Generate risk detections for high-risk interactions
        if data["risk_level"] == "high":
            risk = RiskDetection(
                id=f"risk_{i+1:03d}",
                interaction_id=interaction.id,
                session_id=session1.id,
                organization_id="org_demo",
                risk_type=RiskType.HALLUCINATION,
                risk_score=0.85,
                confidence=0.92,
                description="Potential misinformation about climate change",
                evidence={"confidence_words": 2, "factual_claims": 3},
                detected_at=datetime.now() - timedelta(minutes=25-i*5),
                severity=AlertSeverity.HIGH
            )
            risks_db[risk.id] = risk
        elif data["risk_level"] == "toxic":
            risk = RiskDetection(
                id=f"risk_{i+1:03d}",
                interaction_id=interaction.id,
                session_id=session1.id,
                organization_id="org_demo",
                risk_type=RiskType.TOXICITY,
                risk_score=0.95,
                confidence=0.98,
                description="Toxic language and personal attacks detected",
                evidence={"toxic_words": ["stupid"], "aggressive_tone": True},
                detected_at=datetime.now() - timedelta(minutes=25-i*5),
                severity=AlertSeverity.CRITICAL
            )
            risks_db[risk.id] = risk
        elif data["risk_level"] == "privacy":
            risk = RiskDetection(
                id=f"risk_{i+1:03d}",
                interaction_id=interaction.id,
                session_id=session1.id,
                organization_id="org_demo",
                risk_type=RiskType.PRIVACY_LEAK,
                risk_score=0.90,
                confidence=0.95,
                description="Personal information leaked in response",
                evidence={"ssn_found": 1, "credit_card_found": 1},
                detected_at=datetime.now() - timedelta(minutes=25-i*5),
                severity=AlertSeverity.CRITICAL
            )
            risks_db[risk.id] = risk

# Initialize sample data
initialize_sample_data()


@llm_observability_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get main LLM observability dashboard data"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        time_range = request.args.get('time_range', '24h')  # 1h, 24h, 7d, 30d
        
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
        org_sessions = [s for s in sessions_db.values() if s.organization_id == org_id]
        org_interactions = [i for i in interactions_db.values() 
                          if i.organization_id == org_id and i.timestamp >= start_time]
        org_risks = [r for r in risks_db.values() 
                    if r.organization_id == org_id and r.detected_at >= start_time]
        org_alerts = [a for a in alerts_db.values() 
                     if a.organization_id == org_id and a.triggered_at >= start_time]
        
        # Calculate metrics
        total_interactions = len(org_interactions)
        total_sessions = len(org_sessions)
        total_tokens = sum(i.tokens_input + i.tokens_output for i in org_interactions)
        total_cost = sum(i.cost for i in org_interactions)
        avg_latency = statistics.mean([i.latency_ms for i in org_interactions]) if org_interactions else 0
        
        # Risk metrics
        high_risk_count = len([r for r in org_risks if r.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]])
        risk_rate = (len(org_risks) / total_interactions * 100) if total_interactions > 0 else 0
        
        # Quality metrics (simplified)
        avg_quality = 0.78  # Would be calculated from actual quality assessments
        
        # Model usage
        model_usage = {}
        for interaction in org_interactions:
            model = interaction.model_name
            if model not in model_usage:
                model_usage[model] = 0
            model_usage[model] += 1
        
        # Risk distribution
        risk_distribution = {}
        for risk in org_risks:
            risk_type = risk.risk_type.value
            if risk_type not in risk_distribution:
                risk_distribution[risk_type] = 0
            risk_distribution[risk_type] += 1
        
        return jsonify({
            "status": "success",
            "data": {
                "overview": {
                    "total_interactions": total_interactions,
                    "total_sessions": total_sessions,
                    "total_tokens_processed": total_tokens,
                    "total_cost": round(total_cost, 2),
                    "average_latency_ms": round(avg_latency, 2),
                    "high_risk_interactions": high_risk_count,
                    "risk_detection_rate": round(risk_rate, 2),
                    "average_quality_score": avg_quality,
                    "active_alerts": len([a for a in org_alerts if not a.resolved_at])
                },
                "model_usage": model_usage,
                "risk_distribution": risk_distribution,
                "recent_alerts": [a.to_dict() for a in sorted(org_alerts, key=lambda x: x.triggered_at, reverse=True)[:5]],
                "time_range": time_range,
                "last_updated": datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@llm_observability_bp.route('/interactions', methods=['GET'])
def get_interactions():
    """Get list of LLM interactions with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        session_id = request.args.get('session_id')
        model_name = request.args.get('model_name')
        risk_level = request.args.get('risk_level')  # low, medium, high, critical
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Filter interactions
        filtered_interactions = []
        for interaction in interactions_db.values():
            if interaction.organization_id != org_id:
                continue
            if session_id and interaction.session_id != session_id:
                continue
            if model_name and interaction.model_name != model_name:
                continue
            
            # Check risk level if specified
            if risk_level:
                interaction_risks = [r for r in risks_db.values() if r.interaction_id == interaction.id]
                if risk_level == 'low' and any(r.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL] for r in interaction_risks):
                    continue
                elif risk_level in ['high', 'critical'] and not any(r.severity.value == risk_level for r in interaction_risks):
                    continue
            
            filtered_interactions.append(interaction)
        
        # Sort by timestamp (newest first)
        filtered_interactions.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply pagination
        total_count = len(filtered_interactions)
        paginated_interactions = filtered_interactions[offset:offset + limit]
        
        # Enrich with risk and quality data
        enriched_interactions = []
        for interaction in paginated_interactions:
            interaction_dict = interaction.to_dict()
            
            # Add risk information
            interaction_risks = [r for r in risks_db.values() if r.interaction_id == interaction.id]
            interaction_dict['risks'] = [r.to_dict() for r in interaction_risks]
            interaction_dict['risk_count'] = len(interaction_risks)
            interaction_dict['max_risk_score'] = max([r.risk_score for r in interaction_risks], default=0.0)
            
            # Add quality information (simplified)
            interaction_dict['quality_score'] = 0.75 + (hash(interaction.id) % 25) / 100  # Simulated
            
            enriched_interactions.append(interaction_dict)
        
        return jsonify({
            "status": "success",
            "data": {
                "interactions": enriched_interactions,
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


@llm_observability_bp.route('/interactions', methods=['POST'])
def create_interaction():
    """Create a new LLM interaction and analyze it"""
    try:
        data = request.get_json()
        
        # Create interaction
        interaction = LLMInteraction(
            id=str(uuid.uuid4()),
            session_id=data.get('session_id', str(uuid.uuid4())),
            organization_id=data['organization_id'],
            model_name=data['model_name'],
            prompt=data['prompt'],
            response=data['response'],
            timestamp=datetime.now(),
            latency_ms=data.get('latency_ms', 0),
            tokens_input=data.get('tokens_input', len(data['prompt'].split()) * 1.3),
            tokens_output=data.get('tokens_output', len(data['response'].split()) * 1.3),
            cost=data.get('cost', 0.03),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 150),
            user_id=data.get('user_id')
        )
        
        interactions_db[interaction.id] = interaction
        
        # Perform risk analysis
        risks_detected = []
        
        # Hallucination detection
        hallucination_result = RiskDetectionEngine.detect_hallucination(
            interaction.prompt, interaction.response
        )
        if hallucination_result['risk_score'] > 0.3:
            risk = RiskDetection(
                id=str(uuid.uuid4()),
                interaction_id=interaction.id,
                session_id=interaction.session_id,
                organization_id=interaction.organization_id,
                risk_type=RiskType.HALLUCINATION,
                risk_score=hallucination_result['risk_score'],
                confidence=hallucination_result['confidence'],
                description="Potential hallucination detected",
                evidence=hallucination_result['evidence'],
                detected_at=datetime.now(),
                severity=AlertSeverity.HIGH if hallucination_result['risk_score'] > 0.7 else AlertSeverity.MEDIUM
            )
            risks_db[risk.id] = risk
            risks_detected.append(risk.to_dict())
        
        # Bias detection
        bias_result = RiskDetectionEngine.detect_bias(
            interaction.prompt, interaction.response
        )
        if bias_result['risk_score'] > 0.3:
            risk = RiskDetection(
                id=str(uuid.uuid4()),
                interaction_id=interaction.id,
                session_id=interaction.session_id,
                organization_id=interaction.organization_id,
                risk_type=RiskType.BIAS,
                risk_score=bias_result['risk_score'],
                confidence=bias_result['confidence'],
                description="Potential bias detected",
                evidence=bias_result['evidence'],
                detected_at=datetime.now(),
                severity=AlertSeverity.HIGH if bias_result['risk_score'] > 0.7 else AlertSeverity.MEDIUM
            )
            risks_db[risk.id] = risk
            risks_detected.append(risk.to_dict())
        
        # Toxicity detection
        toxicity_result = RiskDetectionEngine.detect_toxicity(
            interaction.prompt, interaction.response
        )
        if toxicity_result['risk_score'] > 0.2:
            risk = RiskDetection(
                id=str(uuid.uuid4()),
                interaction_id=interaction.id,
                session_id=interaction.session_id,
                organization_id=interaction.organization_id,
                risk_type=RiskType.TOXICITY,
                risk_score=toxicity_result['risk_score'],
                confidence=toxicity_result['confidence'],
                description="Toxic content detected",
                evidence=toxicity_result['evidence'],
                detected_at=datetime.now(),
                severity=AlertSeverity.CRITICAL if toxicity_result['risk_score'] > 0.8 else AlertSeverity.HIGH
            )
            risks_db[risk.id] = risk
            risks_detected.append(risk.to_dict())
        
        # Privacy leak detection
        privacy_result = RiskDetectionEngine.detect_privacy_leak(
            interaction.prompt, interaction.response
        )
        if privacy_result['risk_score'] > 0.1:
            risk = RiskDetection(
                id=str(uuid.uuid4()),
                interaction_id=interaction.id,
                session_id=interaction.session_id,
                organization_id=interaction.organization_id,
                risk_type=RiskType.PRIVACY_LEAK,
                risk_score=privacy_result['risk_score'],
                confidence=privacy_result['confidence'],
                description="Privacy leak detected",
                evidence=privacy_result['evidence'],
                detected_at=datetime.now(),
                severity=AlertSeverity.CRITICAL if privacy_result['risk_score'] > 0.6 else AlertSeverity.HIGH
            )
            risks_db[risk.id] = risk
            risks_detected.append(risk.to_dict())
        
        # Quality assessment
        quality_scores = {
            QualityMetric.RELEVANCE: QualityAssessmentEngine.assess_relevance(interaction.prompt, interaction.response),
            QualityMetric.COHERENCE: QualityAssessmentEngine.assess_coherence(interaction.response),
            QualityMetric.COMPLETENESS: QualityAssessmentEngine.assess_completeness(interaction.prompt, interaction.response),
            QualityMetric.CLARITY: QualityAssessmentEngine.assess_clarity(interaction.response),
            QualityMetric.FACTUALITY: 0.8,  # Would use external fact-checking
            QualityMetric.CREATIVITY: 0.7   # Would use specialized models
        }
        
        overall_quality = sum(quality_scores.values()) / len(quality_scores)
        
        quality_assessment = QualityAssessment(
            id=str(uuid.uuid4()),
            interaction_id=interaction.id,
            session_id=interaction.session_id,
            organization_id=interaction.organization_id,
            overall_score=overall_quality,
            metric_scores=quality_scores,
            assessment_method="automated",
            assessor_id="system",
            assessment_timestamp=datetime.now()
        )
        
        quality_assessments_db[quality_assessment.id] = quality_assessment
        
        return jsonify({
            "status": "success",
            "data": {
                "interaction": interaction.to_dict(),
                "risks_detected": risks_detected,
                "quality_assessment": quality_assessment.to_dict(),
                "analysis_summary": {
                    "total_risks": len(risks_detected),
                    "max_risk_score": max([r['risk_score'] for r in risks_detected], default=0.0),
                    "overall_quality": round(overall_quality, 3),
                    "requires_review": len(risks_detected) > 0 or overall_quality < 0.6
                }
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@llm_observability_bp.route('/risks', methods=['GET'])
def get_risks():
    """Get detected risks with filtering"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        risk_type = request.args.get('risk_type')
        severity = request.args.get('severity')
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Filter risks
        filtered_risks = []
        for risk in risks_db.values():
            if risk.organization_id != org_id:
                continue
            if risk_type and risk.risk_type.value != risk_type:
                continue
            if severity and risk.severity.value != severity:
                continue
            if session_id and risk.session_id != session_id:
                continue
            
            filtered_risks.append(risk)
        
        # Sort by detection time (newest first)
        filtered_risks.sort(key=lambda x: x.detected_at, reverse=True)
        
        # Apply pagination
        total_count = len(filtered_risks)
        paginated_risks = filtered_risks[offset:offset + limit]
        
        return jsonify({
            "status": "success",
            "data": {
                "risks": [r.to_dict() for r in paginated_risks],
                "pagination": {
                    "total_count": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "summary": {
                    "total_risks": total_count,
                    "by_severity": {
                        "critical": len([r for r in filtered_risks if r.severity == AlertSeverity.CRITICAL]),
                        "high": len([r for r in filtered_risks if r.severity == AlertSeverity.HIGH]),
                        "medium": len([r for r in filtered_risks if r.severity == AlertSeverity.MEDIUM]),
                        "low": len([r for r in filtered_risks if r.severity == AlertSeverity.LOW])
                    },
                    "by_type": {
                        risk_type.value: len([r for r in filtered_risks if r.risk_type == risk_type])
                        for risk_type in RiskType
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@llm_observability_bp.route('/performance', methods=['GET'])
def get_performance_metrics():
    """Get performance metrics for models"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        model_name = request.args.get('model_name')
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
        
        # Filter interactions
        filtered_interactions = [
            i for i in interactions_db.values()
            if i.organization_id == org_id and i.timestamp >= start_time
            and (not model_name or i.model_name == model_name)
        ]
        
        if not filtered_interactions:
            return jsonify({
                "status": "success",
                "data": {"message": "No data available for the specified criteria"}
            })
        
        # Calculate performance metrics
        latencies = [i.latency_ms for i in filtered_interactions]
        costs = [i.cost for i in filtered_interactions]
        tokens = [i.tokens_input + i.tokens_output for i in filtered_interactions]
        
        # Group by model for comparison
        model_metrics = {}
        for interaction in filtered_interactions:
            model = interaction.model_name
            if model not in model_metrics:
                model_metrics[model] = {
                    'interactions': [],
                    'total_cost': 0,
                    'total_tokens': 0
                }
            model_metrics[model]['interactions'].append(interaction)
            model_metrics[model]['total_cost'] += interaction.cost
            model_metrics[model]['total_tokens'] += interaction.tokens_input + interaction.tokens_output
        
        # Calculate detailed metrics for each model
        detailed_metrics = {}
        for model, data in model_metrics.items():
            interactions = data['interactions']
            model_latencies = [i.latency_ms for i in interactions]
            
            detailed_metrics[model] = {
                'total_interactions': len(interactions),
                'total_cost': round(data['total_cost'], 2),
                'total_tokens': data['total_tokens'],
                'average_latency': round(statistics.mean(model_latencies), 2),
                'p95_latency': round(statistics.quantiles(model_latencies, n=20)[18], 2) if len(model_latencies) > 1 else model_latencies[0],
                'p99_latency': round(statistics.quantiles(model_latencies, n=100)[98], 2) if len(model_latencies) > 1 else model_latencies[0],
                'cost_per_token': round(data['total_cost'] / data['total_tokens'], 6) if data['total_tokens'] > 0 else 0,
                'cost_per_interaction': round(data['total_cost'] / len(interactions), 4),
                'throughput_per_second': round(len(interactions) / ((now - start_time).total_seconds()), 4)
            }
        
        return jsonify({
            "status": "success",
            "data": {
                "time_range": time_range,
                "period_start": start_time.isoformat(),
                "period_end": now.isoformat(),
                "overall_metrics": {
                    "total_interactions": len(filtered_interactions),
                    "total_cost": round(sum(costs), 2),
                    "total_tokens": sum(tokens),
                    "average_latency": round(statistics.mean(latencies), 2),
                    "p95_latency": round(statistics.quantiles(latencies, n=20)[18], 2) if len(latencies) > 1 else latencies[0],
                    "p99_latency": round(statistics.quantiles(latencies, n=100)[98], 2) if len(latencies) > 1 else latencies[0]
                },
                "model_metrics": detailed_metrics
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@llm_observability_bp.route('/models/compare', methods=['POST'])
def compare_models():
    """Compare performance between different models"""
    try:
        data = request.get_json()
        org_id = data['organization_id']
        models_to_compare = data['models']
        comparison_criteria = data.get('criteria', ['latency', 'cost', 'quality'])
        time_range = data.get('time_range', '7d')
        
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
        
        comparison_results = {}
        
        for model in models_to_compare:
            # Get interactions for this model
            model_interactions = [
                i for i in interactions_db.values()
                if i.organization_id == org_id 
                and i.model_name == model 
                and i.timestamp >= start_time
            ]
            
            if not model_interactions:
                comparison_results[model] = {"error": "No data available"}
                continue
            
            # Calculate metrics
            latencies = [i.latency_ms for i in model_interactions]
            costs = [i.cost for i in model_interactions]
            
            # Get quality scores (simplified)
            quality_scores = [0.75 + (hash(i.id) % 25) / 100 for i in model_interactions]
            
            # Get risk scores
            model_risks = [
                r for r in risks_db.values()
                if any(r.interaction_id == i.id for i in model_interactions)
            ]
            risk_rate = len(model_risks) / len(model_interactions) if model_interactions else 0
            
            comparison_results[model] = {
                "interactions_count": len(model_interactions),
                "average_latency": round(statistics.mean(latencies), 2),
                "average_cost": round(statistics.mean(costs), 4),
                "average_quality": round(statistics.mean(quality_scores), 3),
                "risk_rate": round(risk_rate * 100, 2),
                "total_cost": round(sum(costs), 2),
                "p95_latency": round(statistics.quantiles(latencies, n=20)[18], 2) if len(latencies) > 1 else latencies[0]
            }
        
        # Determine winner for each criterion
        winners = {}
        if 'latency' in comparison_criteria:
            winners['latency'] = min(comparison_results.keys(), 
                                   key=lambda m: comparison_results[m].get('average_latency', float('inf')))
        if 'cost' in comparison_criteria:
            winners['cost'] = min(comparison_results.keys(), 
                                key=lambda m: comparison_results[m].get('average_cost', float('inf')))
        if 'quality' in comparison_criteria:
            winners['quality'] = max(comparison_results.keys(), 
                                   key=lambda m: comparison_results[m].get('average_quality', 0))
        
        # Overall winner (simple scoring)
        model_scores = {}
        for model in models_to_compare:
            if model not in comparison_results or 'error' in comparison_results[model]:
                continue
            
            score = 0
            if 'latency' in comparison_criteria and winners['latency'] == model:
                score += 1
            if 'cost' in comparison_criteria and winners['cost'] == model:
                score += 1
            if 'quality' in comparison_criteria and winners['quality'] == model:
                score += 1
            
            model_scores[model] = score
        
        overall_winner = max(model_scores.keys(), key=lambda m: model_scores[m]) if model_scores else None
        
        # Create comparison record
        comparison = ModelComparison(
            id=str(uuid.uuid4()),
            organization_id=org_id,
            comparison_name=f"Model Comparison {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            models_compared=models_to_compare,
            comparison_period_start=start_time,
            comparison_period_end=now,
            comparison_metrics=comparison_results,
            winner_model=overall_winner or "No clear winner",
            winner_criteria=list(winners.values()),
            detailed_analysis={
                "criteria_winners": winners,
                "model_scores": model_scores,
                "comparison_criteria": comparison_criteria
            },
            created_by="system",
            created_at=datetime.now()
        )
        
        model_comparisons_db[comparison.id] = comparison
        
        return jsonify({
            "status": "success",
            "data": {
                "comparison": comparison.to_dict(),
                "summary": {
                    "overall_winner": overall_winner,
                    "criteria_winners": winners,
                    "models_analyzed": len([m for m in models_to_compare if m in comparison_results and 'error' not in comparison_results[m]])
                }
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@llm_observability_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get LLM observability alerts"""
    try:
        org_id = request.args.get('organization_id', 'org_demo')
        severity = request.args.get('severity')
        status = request.args.get('status', 'active')  # active, acknowledged, resolved
        limit = int(request.args.get('limit', 50))
        
        # Filter alerts
        filtered_alerts = []
        for alert in alerts_db.values():
            if alert.organization_id != org_id:
                continue
            if severity and alert.severity.value != severity:
                continue
            if status == 'active' and alert.acknowledged_at:
                continue
            elif status == 'acknowledged' and (not alert.acknowledged_at or alert.resolved_at):
                continue
            elif status == 'resolved' and not alert.resolved_at:
                continue
            
            filtered_alerts.append(alert)
        
        # Sort by trigger time (newest first)
        filtered_alerts.sort(key=lambda x: x.triggered_at, reverse=True)
        
        # Apply limit
        limited_alerts = filtered_alerts[:limit]
        
        return jsonify({
            "status": "success",
            "data": {
                "alerts": [a.to_dict() for a in limited_alerts],
                "summary": {
                    "total_alerts": len(filtered_alerts),
                    "by_severity": {
                        "critical": len([a for a in filtered_alerts if a.severity == AlertSeverity.CRITICAL]),
                        "high": len([a for a in filtered_alerts if a.severity == AlertSeverity.HIGH]),
                        "medium": len([a for a in filtered_alerts if a.severity == AlertSeverity.MEDIUM]),
                        "low": len([a for a in filtered_alerts if a.severity == AlertSeverity.LOW])
                    }
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@llm_observability_bp.route('/quality/assess', methods=['POST'])
def assess_quality():
    """Manually assess quality of an interaction"""
    try:
        data = request.get_json()
        
        interaction_id = data['interaction_id']
        assessor_id = data['assessor_id']
        metric_scores = data.get('metric_scores', {})
        
        # Get interaction
        if interaction_id not in interactions_db:
            return jsonify({"status": "error", "message": "Interaction not found"}), 404
        
        interaction = interactions_db[interaction_id]
        
        # Convert string keys to QualityMetric enums
        quality_scores = {}
        for metric_str, score in metric_scores.items():
            try:
                metric = QualityMetric(metric_str)
                quality_scores[metric] = float(score)
            except ValueError:
                continue
        
        # Calculate overall score
        overall_score = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0.0
        
        # Create quality assessment
        assessment = QualityAssessment(
            id=str(uuid.uuid4()),
            interaction_id=interaction_id,
            session_id=interaction.session_id,
            organization_id=interaction.organization_id,
            overall_score=overall_score,
            metric_scores=quality_scores,
            assessment_method="human",
            assessor_id=assessor_id,
            assessment_timestamp=datetime.now(),
            feedback_provided=data.get('feedback_provided', False),
            improvement_suggestions=data.get('improvement_suggestions', [])
        )
        
        quality_assessments_db[assessment.id] = assessment
        
        return jsonify({
            "status": "success",
            "data": {
                "assessment": assessment.to_dict(),
                "message": "Quality assessment completed successfully"
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@llm_observability_bp.route('/sessions/<session_id>', methods=['GET'])
def get_session_details():
    """Get detailed information about a specific session"""
    try:
        session_id = request.view_args['session_id']
        
        if session_id not in sessions_db:
            return jsonify({"status": "error", "message": "Session not found"}), 404
        
        session = sessions_db[session_id]
        
        # Get all interactions for this session
        session_interactions = [i for i in interactions_db.values() if i.session_id == session_id]
        session_interactions.sort(key=lambda x: x.timestamp)
        
        # Get all risks for this session
        session_risks = [r for r in risks_db.values() if r.session_id == session_id]
        
        # Get quality assessments
        session_quality = [q for q in quality_assessments_db.values() if q.session_id == session_id]
        
        # Calculate session statistics
        total_tokens = sum(i.tokens_input + i.tokens_output for i in session_interactions)
        total_cost = sum(i.cost for i in session_interactions)
        avg_latency = statistics.mean([i.latency_ms for i in session_interactions]) if session_interactions else 0
        avg_quality = statistics.mean([q.overall_score for q in session_quality]) if session_quality else 0
        
        return jsonify({
            "status": "success",
            "data": {
                "session": session.to_dict(),
                "interactions": [i.to_dict() for i in session_interactions],
                "risks": [r.to_dict() for r in session_risks],
                "quality_assessments": [q.to_dict() for q in session_quality],
                "statistics": {
                    "total_interactions": len(session_interactions),
                    "total_tokens": total_tokens,
                    "total_cost": round(total_cost, 2),
                    "average_latency": round(avg_latency, 2),
                    "average_quality": round(avg_quality, 3),
                    "risk_count": len(session_risks),
                    "high_risk_count": len([r for r in session_risks if r.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]])
                }
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

