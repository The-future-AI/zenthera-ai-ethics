"""
ZenThera AI Ethics Platform
Feature 3: LLM Observability Engine - Data Models

This module defines the data models for comprehensive LLM monitoring,
including performance metrics, risk detection, quality assessment,
and model comparison capabilities.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json


class ModelType(Enum):
    """Supported LLM model types"""
    GPT = "gpt"
    CLAUDE = "claude"
    LLAMA = "llama"
    GEMINI = "gemini"
    CUSTOM = "custom"


class RiskType(Enum):
    """Types of risks detected in LLM outputs"""
    HALLUCINATION = "hallucination"
    BIAS = "bias"
    TOXICITY = "toxicity"
    PRIVACY_LEAK = "privacy_leak"
    MISINFORMATION = "misinformation"
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    COPYRIGHT = "copyright"


class QualityMetric(Enum):
    """Quality assessment metrics"""
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    FACTUALITY = "factuality"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    CREATIVITY = "creativity"


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class LLMSession:
    """Represents a complete LLM interaction session"""
    id: str
    organization_id: str
    model_name: str
    model_type: ModelType
    model_version: str
    user_id: Optional[str]
    session_start: datetime
    session_end: Optional[datetime]
    total_interactions: int
    total_tokens_input: int
    total_tokens_output: int
    total_cost: float
    average_latency: float
    session_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "model_name": self.model_name,
            "model_type": self.model_type.value,
            "model_version": self.model_version,
            "user_id": self.user_id,
            "session_start": self.session_start.isoformat(),
            "session_end": self.session_end.isoformat() if self.session_end else None,
            "total_interactions": self.total_interactions,
            "total_tokens_input": self.total_tokens_input,
            "total_tokens_output": self.total_tokens_output,
            "total_cost": self.total_cost,
            "average_latency": self.average_latency,
            "session_metadata": self.session_metadata
        }


@dataclass
class LLMInteraction:
    """Represents a single LLM interaction (prompt + response)"""
    id: str
    session_id: str
    organization_id: str
    model_name: str
    prompt: str
    response: str
    timestamp: datetime
    latency_ms: float
    tokens_input: int
    tokens_output: int
    cost: float
    temperature: float
    max_tokens: int
    user_id: Optional[str] = None
    interaction_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "organization_id": self.organization_id,
            "model_name": self.model_name,
            "prompt": self.prompt,
            "response": self.response,
            "timestamp": self.timestamp.isoformat(),
            "latency_ms": self.latency_ms,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "cost": self.cost,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "user_id": self.user_id,
            "interaction_metadata": self.interaction_metadata
        }


@dataclass
class RiskDetection:
    """Represents detected risks in LLM interactions"""
    id: str
    interaction_id: str
    session_id: str
    organization_id: str
    risk_type: RiskType
    risk_score: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    description: str
    evidence: Dict[str, Any]
    detected_at: datetime
    severity: AlertSeverity
    is_false_positive: bool = False
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    mitigation_applied: bool = False
    mitigation_details: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "interaction_id": self.interaction_id,
            "session_id": self.session_id,
            "organization_id": self.organization_id,
            "risk_type": self.risk_type.value,
            "risk_score": self.risk_score,
            "confidence": self.confidence,
            "description": self.description,
            "evidence": self.evidence,
            "detected_at": self.detected_at.isoformat(),
            "severity": self.severity.value,
            "is_false_positive": self.is_false_positive,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "mitigation_applied": self.mitigation_applied,
            "mitigation_details": self.mitigation_details
        }


@dataclass
class QualityAssessment:
    """Represents quality assessment of LLM responses"""
    id: str
    interaction_id: str
    session_id: str
    organization_id: str
    overall_score: float  # 0.0 to 1.0
    metric_scores: Dict[QualityMetric, float]
    assessment_method: str  # "automated", "human", "hybrid"
    assessor_id: Optional[str]
    assessment_timestamp: datetime
    feedback_provided: bool = False
    improvement_suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "interaction_id": self.interaction_id,
            "session_id": self.session_id,
            "organization_id": self.organization_id,
            "overall_score": self.overall_score,
            "metric_scores": {metric.value: score for metric, score in self.metric_scores.items()},
            "assessment_method": self.assessment_method,
            "assessor_id": self.assessor_id,
            "assessment_timestamp": self.assessment_timestamp.isoformat(),
            "feedback_provided": self.feedback_provided,
            "improvement_suggestions": self.improvement_suggestions
        }


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics for LLM models"""
    id: str
    organization_id: str
    model_name: str
    time_period_start: datetime
    time_period_end: datetime
    total_interactions: int
    total_sessions: int
    total_tokens_processed: int
    total_cost: float
    average_latency: float
    p95_latency: float
    p99_latency: float
    throughput_per_second: float
    error_rate: float
    success_rate: float
    average_quality_score: float
    risk_detection_rate: float
    top_risk_types: List[str]
    cost_per_token: float
    cost_per_interaction: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "model_name": self.model_name,
            "time_period_start": self.time_period_start.isoformat(),
            "time_period_end": self.time_period_end.isoformat(),
            "total_interactions": self.total_interactions,
            "total_sessions": self.total_sessions,
            "total_tokens_processed": self.total_tokens_processed,
            "total_cost": self.total_cost,
            "average_latency": self.average_latency,
            "p95_latency": self.p95_latency,
            "p99_latency": self.p99_latency,
            "throughput_per_second": self.throughput_per_second,
            "error_rate": self.error_rate,
            "success_rate": self.success_rate,
            "average_quality_score": self.average_quality_score,
            "risk_detection_rate": self.risk_detection_rate,
            "top_risk_types": self.top_risk_types,
            "cost_per_token": self.cost_per_token,
            "cost_per_interaction": self.cost_per_interaction
        }


@dataclass
class ModelComparison:
    """Comparison between different LLM models"""
    id: str
    organization_id: str
    comparison_name: str
    models_compared: List[str]
    comparison_period_start: datetime
    comparison_period_end: datetime
    comparison_metrics: Dict[str, Dict[str, float]]
    winner_model: str
    winner_criteria: List[str]
    detailed_analysis: Dict[str, Any]
    created_by: str
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "comparison_name": self.comparison_name,
            "models_compared": self.models_compared,
            "comparison_period_start": self.comparison_period_start.isoformat(),
            "comparison_period_end": self.comparison_period_end.isoformat(),
            "comparison_metrics": self.comparison_metrics,
            "winner_model": self.winner_model,
            "winner_criteria": self.winner_criteria,
            "detailed_analysis": self.detailed_analysis,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class DriftDetection:
    """Detects performance drift in LLM models over time"""
    id: str
    organization_id: str
    model_name: str
    drift_type: str  # "performance", "quality", "cost", "latency"
    baseline_period_start: datetime
    baseline_period_end: datetime
    current_period_start: datetime
    current_period_end: datetime
    baseline_value: float
    current_value: float
    drift_percentage: float
    drift_direction: str  # "improvement", "degradation", "stable"
    statistical_significance: float
    detected_at: datetime
    alert_triggered: bool
    investigation_status: str = "pending"  # "pending", "investigating", "resolved"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "model_name": self.model_name,
            "drift_type": self.drift_type,
            "baseline_period_start": self.baseline_period_start.isoformat(),
            "baseline_period_end": self.baseline_period_end.isoformat(),
            "current_period_start": self.current_period_start.isoformat(),
            "current_period_end": self.current_period_end.isoformat(),
            "baseline_value": self.baseline_value,
            "current_value": self.current_value,
            "drift_percentage": self.drift_percentage,
            "drift_direction": self.drift_direction,
            "statistical_significance": self.statistical_significance,
            "detected_at": self.detected_at.isoformat(),
            "alert_triggered": self.alert_triggered,
            "investigation_status": self.investigation_status
        }


@dataclass
class LLMAlert:
    """Real-time alerts for LLM observability issues"""
    id: str
    organization_id: str
    alert_type: str  # "risk_detection", "performance_degradation", "cost_spike", "quality_drop"
    severity: AlertSeverity
    title: str
    description: str
    model_name: str
    trigger_value: float
    threshold_value: float
    related_entity_id: str  # interaction_id, session_id, etc.
    related_entity_type: str  # "interaction", "session", "model"
    triggered_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None
    auto_resolved: bool = False
    escalated: bool = False
    escalated_to: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "alert_type": self.alert_type,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "model_name": self.model_name,
            "trigger_value": self.trigger_value,
            "threshold_value": self.threshold_value,
            "related_entity_id": self.related_entity_id,
            "related_entity_type": self.related_entity_type,
            "triggered_at": self.triggered_at.isoformat(),
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "acknowledged_by": self.acknowledged_by,
            "resolved_by": self.resolved_by,
            "resolution_notes": self.resolution_notes,
            "auto_resolved": self.auto_resolved,
            "escalated": self.escalated,
            "escalated_to": self.escalated_to
        }


# Risk Detection Algorithms
class RiskDetectionEngine:
    """Advanced algorithms for detecting various types of risks in LLM outputs"""
    
    @staticmethod
    def detect_hallucination(prompt: str, response: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Detect potential hallucinations in LLM responses"""
        # Simplified hallucination detection logic
        risk_indicators = []
        confidence = 0.0
        
        # Check for factual inconsistencies
        if any(word in response.lower() for word in ["definitely", "certainly", "absolutely"]):
            if not context or not context.get("verified_facts"):
                risk_indicators.append("Overconfident statements without verification")
                confidence += 0.3
        
        # Check for specific dates, numbers, or names that might be fabricated
        import re
        dates = re.findall(r'\b\d{4}\b|\b\d{1,2}/\d{1,2}/\d{4}\b', response)
        if dates and not context:
            risk_indicators.append("Specific dates mentioned without context")
            confidence += 0.2
        
        # Check for contradictions within the response
        sentences = response.split('.')
        if len(sentences) > 2:
            # Simple contradiction detection (would be more sophisticated in practice)
            if "not" in response and "is" in response:
                risk_indicators.append("Potential internal contradictions")
                confidence += 0.1
        
        return {
            "risk_score": min(confidence, 1.0),
            "confidence": confidence,
            "indicators": risk_indicators,
            "evidence": {
                "response_length": len(response),
                "confidence_words": len([w for w in response.lower().split() if w in ["definitely", "certainly", "absolutely"]]),
                "dates_mentioned": dates
            }
        }
    
    @staticmethod
    def detect_bias(prompt: str, response: str, bias_categories: List[str] = None) -> Dict[str, Any]:
        """Detect potential bias in LLM responses"""
        if not bias_categories:
            bias_categories = ["gender", "race", "age", "religion", "nationality"]
        
        risk_indicators = []
        confidence = 0.0
        detected_biases = []
        
        # Gender bias detection
        gender_biased_words = ["he should", "she should", "men are", "women are", "boys are", "girls are"]
        for word in gender_biased_words:
            if word in response.lower():
                risk_indicators.append(f"Potential gender bias: '{word}'")
                detected_biases.append("gender")
                confidence += 0.2
        
        # Stereotypical language detection
        stereotypes = ["all", "always", "never", "typical", "usually"]
        stereotype_count = sum(1 for word in stereotypes if word in response.lower())
        if stereotype_count > 2:
            risk_indicators.append("High use of generalizing language")
            confidence += 0.1 * stereotype_count
        
        return {
            "risk_score": min(confidence, 1.0),
            "confidence": confidence,
            "indicators": risk_indicators,
            "detected_biases": list(set(detected_biases)),
            "evidence": {
                "stereotype_words": stereotype_count,
                "response_length": len(response)
            }
        }
    
    @staticmethod
    def detect_toxicity(prompt: str, response: str) -> Dict[str, Any]:
        """Detect toxic content in LLM responses"""
        toxic_words = [
            "hate", "stupid", "idiot", "kill", "die", "murder", "violence",
            "racist", "sexist", "discrimination", "harassment"
        ]
        
        risk_indicators = []
        confidence = 0.0
        toxic_words_found = []
        
        response_lower = response.lower()
        for word in toxic_words:
            if word in response_lower:
                toxic_words_found.append(word)
                risk_indicators.append(f"Toxic language detected: '{word}'")
                confidence += 0.3
        
        # Check for aggressive tone
        aggressive_patterns = ["you are", "you're so", "shut up", "go away"]
        for pattern in aggressive_patterns:
            if pattern in response_lower:
                risk_indicators.append(f"Aggressive tone: '{pattern}'")
                confidence += 0.2
        
        return {
            "risk_score": min(confidence, 1.0),
            "confidence": confidence,
            "indicators": risk_indicators,
            "toxic_words": toxic_words_found,
            "evidence": {
                "toxic_word_count": len(toxic_words_found),
                "response_length": len(response)
            }
        }
    
    @staticmethod
    def detect_privacy_leak(prompt: str, response: str) -> Dict[str, Any]:
        """Detect potential privacy leaks in LLM responses"""
        import re
        
        risk_indicators = []
        confidence = 0.0
        leaked_data_types = []
        
        # Email detection
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response)
        if emails:
            risk_indicators.append(f"Email addresses detected: {len(emails)}")
            leaked_data_types.append("email")
            confidence += 0.4
        
        # Phone number detection
        phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', response)
        if phones:
            risk_indicators.append(f"Phone numbers detected: {len(phones)}")
            leaked_data_types.append("phone")
            confidence += 0.4
        
        # Credit card detection
        credit_cards = re.findall(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', response)
        if credit_cards:
            risk_indicators.append(f"Credit card patterns detected: {len(credit_cards)}")
            leaked_data_types.append("credit_card")
            confidence += 0.6
        
        # SSN detection
        ssns = re.findall(r'\b\d{3}-\d{2}-\d{4}\b', response)
        if ssns:
            risk_indicators.append(f"SSN patterns detected: {len(ssns)}")
            leaked_data_types.append("ssn")
            confidence += 0.8
        
        return {
            "risk_score": min(confidence, 1.0),
            "confidence": confidence,
            "indicators": risk_indicators,
            "leaked_data_types": leaked_data_types,
            "evidence": {
                "emails_found": emails,
                "phones_found": phones,
                "credit_cards_found": len(credit_cards),
                "ssns_found": len(ssns)
            }
        }


# Quality Assessment Engine
class QualityAssessmentEngine:
    """Advanced algorithms for assessing LLM response quality"""
    
    @staticmethod
    def assess_relevance(prompt: str, response: str) -> float:
        """Assess how relevant the response is to the prompt"""
        # Simplified relevance scoring
        prompt_words = set(prompt.lower().split())
        response_words = set(response.lower().split())
        
        # Calculate word overlap
        overlap = len(prompt_words.intersection(response_words))
        total_prompt_words = len(prompt_words)
        
        if total_prompt_words == 0:
            return 0.0
        
        relevance_score = min(overlap / total_prompt_words, 1.0)
        
        # Boost score if response directly addresses the prompt
        if any(word in response.lower() for word in ["answer", "solution", "result", "conclusion"]):
            relevance_score = min(relevance_score + 0.2, 1.0)
        
        return relevance_score
    
    @staticmethod
    def assess_coherence(response: str) -> float:
        """Assess the coherence and logical flow of the response"""
        sentences = response.split('.')
        if len(sentences) < 2:
            return 0.5  # Single sentence, moderate coherence
        
        # Check for transition words
        transition_words = ["however", "therefore", "furthermore", "additionally", "consequently", "meanwhile"]
        transition_count = sum(1 for sentence in sentences for word in transition_words if word in sentence.lower())
        
        # Check for logical connectors
        connectors = ["because", "since", "as a result", "due to", "leads to", "causes"]
        connector_count = sum(1 for sentence in sentences for word in connectors if word in sentence.lower())
        
        # Calculate coherence score
        coherence_score = 0.5  # Base score
        coherence_score += min(transition_count * 0.1, 0.3)
        coherence_score += min(connector_count * 0.1, 0.2)
        
        return min(coherence_score, 1.0)
    
    @staticmethod
    def assess_completeness(prompt: str, response: str) -> float:
        """Assess how complete the response is"""
        # Check if response addresses all parts of a multi-part question
        question_indicators = ["what", "how", "why", "when", "where", "who"]
        questions_in_prompt = sum(1 for indicator in question_indicators if indicator in prompt.lower())
        
        if questions_in_prompt == 0:
            return 0.8  # Not a question, assume complete
        
        # Check if response provides comprehensive coverage
        response_length = len(response.split())
        if response_length < 10:
            return 0.3  # Too short
        elif response_length < 50:
            return 0.6  # Moderate length
        else:
            return 0.9  # Comprehensive
    
    @staticmethod
    def assess_clarity(response: str) -> float:
        """Assess the clarity and readability of the response"""
        words = response.split()
        sentences = response.split('.')
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.0
        
        # Calculate average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Optimal sentence length is around 15-20 words
        if 10 <= avg_sentence_length <= 25:
            length_score = 1.0
        elif 5 <= avg_sentence_length < 10 or 25 < avg_sentence_length <= 35:
            length_score = 0.7
        else:
            length_score = 0.4
        
        # Check for complex words (more than 3 syllables - simplified)
        complex_words = [word for word in words if len(word) > 8]
        complexity_ratio = len(complex_words) / len(words)
        
        complexity_score = 1.0 - min(complexity_ratio * 2, 0.5)
        
        return (length_score + complexity_score) / 2

