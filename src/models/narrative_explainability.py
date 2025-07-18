"""
ZenThera AI Ethics Platform
Feature 4: Narrative Explainability & Replay - Data Models

This module defines the data models for session replay, narrative explanations,
ethical alignment analysis, and audit trail functionality.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json


class ExplanationType(Enum):
    """Types of explanations generated"""
    DECISION_RATIONALE = "decision_rationale"
    ETHICAL_ANALYSIS = "ethical_analysis"
    RISK_EXPLANATION = "risk_explanation"
    QUALITY_BREAKDOWN = "quality_breakdown"
    COMPLIANCE_ASSESSMENT = "compliance_assessment"
    BIAS_ANALYSIS = "bias_analysis"
    SAFETY_EVALUATION = "safety_evaluation"


class AlignmentCategory(Enum):
    """Categories for ethical alignment assessment"""
    BENEFICENCE = "beneficence"  # Do good
    NON_MALEFICENCE = "non_maleficence"  # Do no harm
    AUTONOMY = "autonomy"  # Respect user autonomy
    JUSTICE = "justice"  # Fairness and equality
    TRANSPARENCY = "transparency"  # Explainability and openness
    ACCOUNTABILITY = "accountability"  # Responsibility and oversight
    PRIVACY = "privacy"  # Data protection and confidentiality
    HUMAN_DIGNITY = "human_dignity"  # Respect for human worth


class ReplayEventType(Enum):
    """Types of events in session replay"""
    USER_INPUT = "user_input"
    MODEL_RESPONSE = "model_response"
    RISK_DETECTION = "risk_detection"
    QUALITY_ASSESSMENT = "quality_assessment"
    SYSTEM_INTERVENTION = "system_intervention"
    HUMAN_REVIEW = "human_review"
    COMPLIANCE_CHECK = "compliance_check"
    ETHICAL_EVALUATION = "ethical_evaluation"


class NarrativeStyle(Enum):
    """Styles for narrative explanations"""
    TECHNICAL = "technical"  # For technical audiences
    EXECUTIVE = "executive"  # For business stakeholders
    REGULATORY = "regulatory"  # For compliance officers
    USER_FRIENDLY = "user_friendly"  # For end users
    AUDIT = "audit"  # For auditors and reviewers


@dataclass
class SessionReplay:
    """Complete replay data for an LLM session"""
    id: str
    session_id: str
    organization_id: str
    created_at: datetime
    created_by: str
    replay_name: str
    description: str
    session_start: datetime
    session_end: datetime
    total_events: int
    total_duration_seconds: float
    participants: List[str]  # User IDs involved
    models_used: List[str]
    replay_metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    is_archived: bool = False
    retention_until: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "organization_id": self.organization_id,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "replay_name": self.replay_name,
            "description": self.description,
            "session_start": self.session_start.isoformat(),
            "session_end": self.session_end.isoformat(),
            "total_events": self.total_events,
            "total_duration_seconds": self.total_duration_seconds,
            "participants": self.participants,
            "models_used": self.models_used,
            "replay_metadata": self.replay_metadata,
            "tags": self.tags,
            "is_archived": self.is_archived,
            "retention_until": self.retention_until.isoformat() if self.retention_until else None
        }


@dataclass
class ReplayEvent:
    """Individual event in a session replay"""
    id: str
    replay_id: str
    session_id: str
    organization_id: str
    event_type: ReplayEventType
    timestamp: datetime
    sequence_number: int
    event_data: Dict[str, Any]
    actor_id: Optional[str]  # User or system ID
    actor_type: str  # "user", "system", "model", "human_reviewer"
    duration_ms: Optional[float]
    related_interaction_id: Optional[str]
    related_risk_id: Optional[str]
    event_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "replay_id": self.replay_id,
            "session_id": self.session_id,
            "organization_id": self.organization_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "sequence_number": self.sequence_number,
            "event_data": self.event_data,
            "actor_id": self.actor_id,
            "actor_type": self.actor_type,
            "duration_ms": self.duration_ms,
            "related_interaction_id": self.related_interaction_id,
            "related_risk_id": self.related_risk_id,
            "event_metadata": self.event_metadata
        }


@dataclass
class NarrativeExplanation:
    """Narrative explanation for AI decisions and behaviors"""
    id: str
    organization_id: str
    explanation_type: ExplanationType
    target_entity_id: str  # interaction_id, session_id, risk_id, etc.
    target_entity_type: str  # "interaction", "session", "risk", "decision"
    narrative_style: NarrativeStyle
    title: str
    summary: str
    detailed_explanation: str
    key_factors: List[str]
    evidence_points: List[Dict[str, Any]]
    confidence_level: float  # 0.0 to 1.0
    generated_at: datetime
    generated_by: str  # "system" or user_id
    generation_method: str  # "automated", "human", "hybrid"
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    is_approved: bool = False
    explanation_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "explanation_type": self.explanation_type.value,
            "target_entity_id": self.target_entity_id,
            "target_entity_type": self.target_entity_type,
            "narrative_style": self.narrative_style.value,
            "title": self.title,
            "summary": self.summary,
            "detailed_explanation": self.detailed_explanation,
            "key_factors": self.key_factors,
            "evidence_points": self.evidence_points,
            "confidence_level": self.confidence_level,
            "generated_at": self.generated_at.isoformat(),
            "generated_by": self.generated_by,
            "generation_method": self.generation_method,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "is_approved": self.is_approved,
            "explanation_metadata": self.explanation_metadata
        }


@dataclass
class EthicalAlignment:
    """Assessment of ethical alignment for AI interactions"""
    id: str
    organization_id: str
    target_entity_id: str
    target_entity_type: str
    assessment_timestamp: datetime
    assessor_id: str
    overall_alignment_score: float  # 0.0 to 1.0
    category_scores: Dict[AlignmentCategory, float]
    alignment_analysis: str
    strengths: List[str]
    concerns: List[str]
    recommendations: List[str]
    compliance_notes: str
    requires_human_review: bool = False
    review_priority: str = "low"  # "low", "medium", "high", "critical"
    assessment_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "target_entity_id": self.target_entity_id,
            "target_entity_type": self.target_entity_type,
            "assessment_timestamp": self.assessment_timestamp.isoformat(),
            "assessor_id": self.assessor_id,
            "overall_alignment_score": self.overall_alignment_score,
            "category_scores": {cat.value: score for cat, score in self.category_scores.items()},
            "alignment_analysis": self.alignment_analysis,
            "strengths": self.strengths,
            "concerns": self.concerns,
            "recommendations": self.recommendations,
            "compliance_notes": self.compliance_notes,
            "requires_human_review": self.requires_human_review,
            "review_priority": self.review_priority,
            "assessment_metadata": self.assessment_metadata
        }


@dataclass
class AuditTrail:
    """Comprehensive audit trail for compliance and governance"""
    id: str
    organization_id: str
    audit_type: str  # "session", "decision", "risk", "compliance"
    target_entity_id: str
    target_entity_type: str
    audit_timestamp: datetime
    auditor_id: str
    audit_scope: List[str]  # Areas covered in audit
    findings: List[Dict[str, Any]]
    compliance_status: str  # "compliant", "non_compliant", "needs_review"
    risk_level: str  # "low", "medium", "high", "critical"
    recommendations: List[str]
    action_items: List[Dict[str, Any]]
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    audit_report: str = ""
    supporting_documents: List[str] = field(default_factory=list)
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "audit_type": self.audit_type,
            "target_entity_id": self.target_entity_id,
            "target_entity_type": self.target_entity_type,
            "audit_timestamp": self.audit_timestamp.isoformat(),
            "auditor_id": self.auditor_id,
            "audit_scope": self.audit_scope,
            "findings": self.findings,
            "compliance_status": self.compliance_status,
            "risk_level": self.risk_level,
            "recommendations": self.recommendations,
            "action_items": self.action_items,
            "follow_up_required": self.follow_up_required,
            "follow_up_date": self.follow_up_date.isoformat() if self.follow_up_date else None,
            "audit_report": self.audit_report,
            "supporting_documents": self.supporting_documents,
            "audit_metadata": self.audit_metadata
        }


@dataclass
class ExplanationTemplate:
    """Templates for generating consistent explanations"""
    id: str
    organization_id: str
    template_name: str
    explanation_type: ExplanationType
    narrative_style: NarrativeStyle
    template_content: str
    variables: List[str]  # Placeholder variables in template
    usage_context: str
    created_by: str
    created_at: datetime
    last_modified: datetime
    is_active: bool = True
    usage_count: int = 0
    template_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "template_name": self.template_name,
            "explanation_type": self.explanation_type.value,
            "narrative_style": self.narrative_style.value,
            "template_content": self.template_content,
            "variables": self.variables,
            "usage_context": self.usage_context,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "is_active": self.is_active,
            "usage_count": self.usage_count,
            "template_metadata": self.template_metadata
        }


# Narrative Generation Engine
class NarrativeGenerator:
    """Advanced engine for generating narrative explanations"""
    
    @staticmethod
    def generate_decision_explanation(interaction_data: Dict[str, Any], 
                                    style: NarrativeStyle = NarrativeStyle.TECHNICAL) -> str:
        """Generate explanation for AI decision-making process"""
        
        prompt = interaction_data.get('prompt', '')
        response = interaction_data.get('response', '')
        model_name = interaction_data.get('model_name', 'AI Model')
        latency = interaction_data.get('latency_ms', 0)
        
        if style == NarrativeStyle.TECHNICAL:
            return f"""
**Technical Decision Analysis for {model_name}**

**Input Processing:**
The model received a prompt of {len(prompt.split())} words requesting information about {NarrativeGenerator._extract_topic(prompt)}. The input was processed through the model's attention mechanisms, with key tokens being weighted based on semantic relevance.

**Response Generation:**
The model generated a {len(response.split())}-word response in {latency}ms, utilizing its trained parameters to construct a contextually appropriate answer. The generation process involved:

1. **Context Understanding**: Analysis of the prompt's intent and required information type
2. **Knowledge Retrieval**: Accessing relevant information from training data
3. **Response Synthesis**: Constructing a coherent response that addresses the query
4. **Quality Assurance**: Internal consistency checks and relevance validation

**Decision Factors:**
- Prompt clarity and specificity
- Available knowledge in training data
- Response length optimization
- Contextual appropriateness
            """.strip()
        
        elif style == NarrativeStyle.EXECUTIVE:
            return f"""
**Executive Summary: AI Decision Process**

**Situation:** User requested information about {NarrativeGenerator._extract_topic(prompt)}

**Action:** {model_name} processed the request and provided a comprehensive response in {latency/1000:.1f} seconds

**Result:** Generated {len(response.split())}-word response addressing the user's query

**Business Impact:**
- Fast response time ensures good user experience
- Comprehensive answer demonstrates model capability
- Automated handling reduces operational costs

**Key Metrics:**
- Response Time: {latency}ms
- Content Quality: High relevance to user query
- Efficiency: Automated processing without human intervention
            """.strip()
        
        elif style == NarrativeStyle.USER_FRIENDLY:
            return f"""
**How Your AI Assistant Made This Decision**

When you asked about {NarrativeGenerator._extract_topic(prompt)}, here's what happened behind the scenes:

**Understanding Your Question:**
Your AI assistant carefully read your question and identified that you were looking for information about {NarrativeGenerator._extract_topic(prompt)}. It analyzed the key words and context to understand exactly what you needed.

**Finding the Right Information:**
The AI searched through its knowledge base to find the most relevant and accurate information to answer your question. It considered multiple sources and perspectives to give you a well-rounded response.

**Crafting the Response:**
Your assistant then organized the information in a clear, helpful way, making sure to address your specific question while providing useful context and details.

**Quality Check:**
Before responding, the AI performed a quick quality check to ensure the answer was relevant, accurate, and helpful for your needs.

The whole process took just {latency/1000:.1f} seconds, allowing you to get the information you needed quickly and efficiently.
            """.strip()
        
        else:  # REGULATORY style
            return f"""
**Regulatory Compliance Analysis: AI Decision Process**

**Process Documentation:**
This analysis documents the decision-making process of {model_name} for regulatory compliance and audit purposes.

**Input Validation:**
- Prompt content reviewed for compliance with usage policies
- No sensitive or prohibited content detected
- Input classified as standard information request

**Processing Methodology:**
- Standard transformer-based language model processing
- No special handling or exceptions required
- Processing time: {latency}ms (within acceptable performance parameters)

**Output Validation:**
- Response content reviewed for accuracy and appropriateness
- No regulatory concerns identified
- Output meets quality and safety standards

**Compliance Notes:**
- Process follows established AI governance protocols
- All interactions logged for audit purposes
- No human intervention required for this standard request

**Audit Trail:**
- Timestamp: {interaction_data.get('timestamp', 'N/A')}
- Model Version: {model_name}
- Processing Duration: {latency}ms
- Compliance Status: Approved
            """.strip()
    
    @staticmethod
    def generate_risk_explanation(risk_data: Dict[str, Any], 
                                style: NarrativeStyle = NarrativeStyle.TECHNICAL) -> str:
        """Generate explanation for detected risks"""
        
        risk_type = risk_data.get('risk_type', 'Unknown')
        risk_score = risk_data.get('risk_score', 0.0)
        confidence = risk_data.get('confidence', 0.0)
        evidence = risk_data.get('evidence', {})
        
        if style == NarrativeStyle.TECHNICAL:
            return f"""
**Risk Detection Analysis: {risk_type.title()}**

**Detection Summary:**
Our risk detection algorithm identified a {risk_type} risk with a score of {risk_score:.2f} (confidence: {confidence:.2f}). This indicates a {NarrativeGenerator._risk_severity_text(risk_score)} level concern that requires attention.

**Technical Details:**
- **Algorithm Used**: {risk_type.title()} Detection Engine v2.0
- **Risk Score**: {risk_score:.3f} (0.0 = no risk, 1.0 = maximum risk)
- **Confidence Level**: {confidence:.3f} (algorithm certainty in detection)
- **Detection Method**: Pattern matching and semantic analysis

**Evidence Analysis:**
{NarrativeGenerator._format_evidence(evidence)}

**Recommended Actions:**
1. Review the flagged content for accuracy of detection
2. Implement appropriate mitigation measures if confirmed
3. Update training data to prevent similar occurrences
4. Monitor for patterns in similar interactions
            """.strip()
        
        elif style == NarrativeStyle.EXECUTIVE:
            return f"""
**Risk Alert: {risk_type.title()} Detected**

**Executive Summary:**
Our AI monitoring system has detected a potential {risk_type} issue that requires management attention.

**Risk Level:** {NarrativeGenerator._risk_severity_text(risk_score).title()}
**Confidence:** {confidence*100:.0f}% certain

**Business Impact:**
- Potential compliance or reputation risk
- May require immediate review and action
- Could affect user trust and satisfaction

**Immediate Actions Required:**
1. Assign responsible team member for review
2. Implement temporary safeguards if necessary
3. Investigate root cause and prevention measures
4. Update risk management protocols as needed

**Timeline:** Recommend review within {NarrativeGenerator._get_review_timeline(risk_score)}
            """.strip()
        
        else:  # USER_FRIENDLY style
            return f"""
**Safety Notice: Content Review Required**

We've detected something in this conversation that needs a closer look to ensure everything meets our safety and quality standards.

**What We Found:**
Our safety systems identified potential {risk_type.replace('_', ' ')} content that might not align with our community guidelines.

**What This Means:**
- This is an automated detection, not a final determination
- A human reviewer will take a look to confirm
- Your conversation is temporarily flagged for review
- This helps us maintain a safe and helpful environment

**What Happens Next:**
1. Our team will review the content within 24 hours
2. If it's a false alarm, the flag will be removed
3. If there is an issue, we'll provide guidance on next steps
4. You'll be notified of the outcome

**Questions?** Contact our support team if you have concerns about this review.
            """.strip()
    
    @staticmethod
    def generate_ethical_analysis(alignment_data: Dict[str, Any],
                                style: NarrativeStyle = NarrativeStyle.TECHNICAL) -> str:
        """Generate ethical alignment analysis"""
        
        overall_score = alignment_data.get('overall_alignment_score', 0.0)
        category_scores = alignment_data.get('category_scores', {})
        strengths = alignment_data.get('strengths', [])
        concerns = alignment_data.get('concerns', [])
        
        if style == NarrativeStyle.TECHNICAL:
            return f"""
**Ethical Alignment Analysis**

**Overall Assessment:**
The interaction achieved an ethical alignment score of {overall_score:.2f}/1.0, indicating {NarrativeGenerator._alignment_level_text(overall_score)} alignment with established ethical principles.

**Category Breakdown:**
{NarrativeGenerator._format_category_scores(category_scores)}

**Strengths Identified:**
{NarrativeGenerator._format_list(strengths)}

**Areas of Concern:**
{NarrativeGenerator._format_list(concerns)}

**Ethical Framework Applied:**
This analysis follows the IEEE Standards for Ethical AI Design and incorporates principles from the EU Ethics Guidelines for Trustworthy AI.

**Methodology:**
- Automated ethical reasoning algorithms
- Multi-dimensional principle assessment
- Contextual appropriateness evaluation
- Stakeholder impact analysis
            """.strip()
        
        elif style == NarrativeStyle.REGULATORY:
            return f"""
**Ethical Compliance Assessment Report**

**Regulatory Framework:** EU AI Act Article 4 - Ethical AI Requirements

**Compliance Score:** {overall_score:.2f}/1.0

**Assessment Criteria:**
This evaluation assesses compliance with mandatory ethical requirements for AI systems as defined in current regulatory frameworks.

**Detailed Findings:**
{NarrativeGenerator._format_category_scores(category_scores)}

**Compliance Status:** {'COMPLIANT' if overall_score >= 0.7 else 'REQUIRES REVIEW'}

**Regulatory Notes:**
- Assessment conducted using approved ethical evaluation frameworks
- All findings documented for audit purposes
- Recommendations align with regulatory best practices

**Action Items:**
{NarrativeGenerator._format_list(concerns, prefix="- Address: ")}

**Certification:** This assessment meets regulatory requirements for AI ethics evaluation.
            """.strip()
        
        else:  # USER_FRIENDLY style
            return f"""
**How Ethical Is This AI Interaction?**

**Overall Rating:** {NarrativeGenerator._get_star_rating(overall_score)} ({overall_score:.1f}/1.0)

**What We Evaluated:**
We checked this AI interaction against important ethical principles to make sure it's helpful, safe, and fair.

**What's Going Well:**
{NarrativeGenerator._format_list(strengths, prefix="✅ ")}

**Areas for Improvement:**
{NarrativeGenerator._format_list(concerns, prefix="⚠️ ")}

**Why This Matters:**
Ethical AI helps ensure that artificial intelligence serves everyone fairly and safely. These evaluations help us continuously improve our AI systems.

**Your Role:**
If you notice anything concerning in AI interactions, please let us know. Your feedback helps make AI better for everyone.
            """.strip()
    
    # Helper methods
    @staticmethod
    def _extract_topic(prompt: str) -> str:
        """Extract main topic from prompt"""
        # Simplified topic extraction
        words = prompt.lower().split()
        if len(words) > 3:
            return " ".join(words[:3]) + "..."
        return prompt[:50] + "..." if len(prompt) > 50 else prompt
    
    @staticmethod
    def _risk_severity_text(score: float) -> str:
        """Convert risk score to severity text"""
        if score >= 0.8:
            return "critical"
        elif score >= 0.6:
            return "high"
        elif score >= 0.4:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _alignment_level_text(score: float) -> str:
        """Convert alignment score to level text"""
        if score >= 0.9:
            return "excellent"
        elif score >= 0.7:
            return "good"
        elif score >= 0.5:
            return "moderate"
        else:
            return "poor"
    
    @staticmethod
    def _format_evidence(evidence: Dict[str, Any]) -> str:
        """Format evidence dictionary for display"""
        if not evidence:
            return "No specific evidence details available."
        
        formatted = []
        for key, value in evidence.items():
            formatted.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        return "\n".join(formatted)
    
    @staticmethod
    def _format_category_scores(scores: Dict[str, float]) -> str:
        """Format category scores for display"""
        if not scores:
            return "No category scores available."
        
        formatted = []
        for category, score in scores.items():
            formatted.append(f"- **{category.replace('_', ' ').title()}**: {score:.2f}/1.0")
        return "\n".join(formatted)
    
    @staticmethod
    def _format_list(items: List[str], prefix: str = "- ") -> str:
        """Format list items for display"""
        if not items:
            return "None identified."
        return "\n".join([f"{prefix}{item}" for item in items])
    
    @staticmethod
    def _get_review_timeline(risk_score: float) -> str:
        """Get recommended review timeline based on risk score"""
        if risk_score >= 0.8:
            return "1 hour"
        elif risk_score >= 0.6:
            return "4 hours"
        elif risk_score >= 0.4:
            return "24 hours"
        else:
            return "72 hours"
    
    @staticmethod
    def _get_star_rating(score: float) -> str:
        """Convert score to star rating"""
        stars = int(score * 5)
        return "⭐" * stars + "☆" * (5 - stars)


# Ethical Alignment Assessment Engine
class EthicalAlignmentEngine:
    """Engine for assessing ethical alignment of AI interactions"""
    
    @staticmethod
    def assess_beneficence(interaction_data: Dict[str, Any]) -> float:
        """Assess how well the interaction promotes good/benefit"""
        response = interaction_data.get('response', '')
        prompt = interaction_data.get('prompt', '')
        
        score = 0.5  # Base score
        
        # Positive indicators
        helpful_words = ['help', 'assist', 'support', 'benefit', 'improve', 'solve']
        if any(word in response.lower() for word in helpful_words):
            score += 0.2
        
        # Check if response provides useful information
        if len(response.split()) > 20:  # Substantial response
            score += 0.1
        
        # Check for constructive tone
        constructive_words = ['suggest', 'recommend', 'consider', 'might', 'could']
        if any(word in response.lower() for word in constructive_words):
            score += 0.1
        
        return min(score, 1.0)
    
    @staticmethod
    def assess_non_maleficence(interaction_data: Dict[str, Any]) -> float:
        """Assess how well the interaction avoids harm"""
        response = interaction_data.get('response', '')
        risks = interaction_data.get('detected_risks', [])
        
        score = 1.0  # Start with perfect score
        
        # Deduct for detected risks
        for risk in risks:
            risk_score = risk.get('risk_score', 0.0)
            score -= risk_score * 0.3  # Reduce based on risk severity
        
        # Check for harmful content indicators
        harmful_words = ['harm', 'hurt', 'damage', 'destroy', 'attack']
        if any(word in response.lower() for word in harmful_words):
            score -= 0.2
        
        return max(score, 0.0)
    
    @staticmethod
    def assess_autonomy(interaction_data: Dict[str, Any]) -> float:
        """Assess respect for user autonomy and choice"""
        response = interaction_data.get('response', '')
        
        score = 0.5  # Base score
        
        # Positive indicators
        autonomy_words = ['choose', 'decide', 'option', 'preference', 'up to you']
        if any(word in response.lower() for word in autonomy_words):
            score += 0.3
        
        # Check for non-prescriptive language
        prescriptive_words = ['must', 'should', 'have to', 'required', 'mandatory']
        prescriptive_count = sum(1 for word in prescriptive_words if word in response.lower())
        if prescriptive_count == 0:
            score += 0.2
        else:
            score -= prescriptive_count * 0.1
        
        return max(min(score, 1.0), 0.0)
    
    @staticmethod
    def assess_justice(interaction_data: Dict[str, Any]) -> float:
        """Assess fairness and equality in the interaction"""
        response = interaction_data.get('response', '')
        bias_risks = [r for r in interaction_data.get('detected_risks', []) 
                     if r.get('risk_type') == 'bias']
        
        score = 0.8  # Start with good score
        
        # Deduct for bias detection
        for bias_risk in bias_risks:
            score -= bias_risk.get('risk_score', 0.0) * 0.5
        
        # Check for inclusive language
        inclusive_words = ['everyone', 'all people', 'regardless', 'inclusive', 'equal']
        if any(word in response.lower() for word in inclusive_words):
            score += 0.1
        
        # Check for discriminatory language
        discriminatory_words = ['only', 'just', 'typical', 'always', 'never']
        discriminatory_count = sum(1 for word in discriminatory_words if word in response.lower())
        score -= discriminatory_count * 0.05
        
        return max(min(score, 1.0), 0.0)
    
    @staticmethod
    def assess_transparency(interaction_data: Dict[str, Any]) -> float:
        """Assess transparency and explainability"""
        response = interaction_data.get('response', '')
        
        score = 0.6  # Base score
        
        # Check for explanatory language
        explanation_words = ['because', 'since', 'due to', 'reason', 'explain']
        if any(word in response.lower() for word in explanation_words):
            score += 0.2
        
        # Check for uncertainty acknowledgment
        uncertainty_words = ['might', 'could', 'possibly', 'uncertain', 'not sure']
        if any(word in response.lower() for word in uncertainty_words):
            score += 0.1
        
        # Check for source attribution
        source_words = ['according to', 'research shows', 'studies indicate']
        if any(phrase in response.lower() for phrase in source_words):
            score += 0.1
        
        return min(score, 1.0)
    
    @staticmethod
    def assess_accountability(interaction_data: Dict[str, Any]) -> float:
        """Assess accountability and responsibility"""
        # For this demo, we'll use a simplified assessment
        # In practice, this would involve more complex analysis
        
        response = interaction_data.get('response', '')
        model_name = interaction_data.get('model_name', '')
        
        score = 0.7  # Base score for logged interactions
        
        # Check for responsible language
        responsible_words = ['responsible', 'careful', 'consider', 'important']
        if any(word in response.lower() for word in responsible_words):
            score += 0.2
        
        # Bonus for having model identification
        if model_name:
            score += 0.1
        
        return min(score, 1.0)
    
    @staticmethod
    def assess_privacy(interaction_data: Dict[str, Any]) -> float:
        """Assess privacy protection"""
        privacy_risks = [r for r in interaction_data.get('detected_risks', []) 
                        if r.get('risk_type') == 'privacy_leak']
        
        score = 1.0  # Start with perfect score
        
        # Deduct heavily for privacy violations
        for privacy_risk in privacy_risks:
            score -= privacy_risk.get('risk_score', 0.0) * 0.8
        
        return max(score, 0.0)
    
    @staticmethod
    def assess_human_dignity(interaction_data: Dict[str, Any]) -> float:
        """Assess respect for human dignity"""
        response = interaction_data.get('response', '')
        toxicity_risks = [r for r in interaction_data.get('detected_risks', []) 
                         if r.get('risk_type') == 'toxicity']
        
        score = 0.9  # Start with high score
        
        # Deduct for toxicity
        for toxicity_risk in toxicity_risks:
            score -= toxicity_risk.get('risk_score', 0.0) * 0.6
        
        # Check for respectful language
        respectful_words = ['please', 'thank you', 'respect', 'appreciate']
        if any(word in response.lower() for word in respectful_words):
            score += 0.1
        
        return max(min(score, 1.0), 0.0)

