"""
ZenThera Compliance Grid - Modelos de Dados
Este arquivo define como organizamos as informações de compliance no banco de dados
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Importar o banco de dados do template
from models.user import db

class ComplianceScore(db.Model):
    """
    Modelo para armazenar scores de compliance AI Act
    Pense nisso como uma "nota" que damos para cada sistema de IA
    """
    __tablename__ = 'compliance_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), nullable=False)  # Qual empresa
    system_name = db.Column(db.String(200), nullable=False)      # Nome do sistema de IA
    
    # Scores individuais (0-100)
    bias_score = db.Column(db.Float, default=0.0)               # Quão justo é o sistema
    transparency_score = db.Column(db.Float, default=0.0)       # Quão explicável é
    logs_score = db.Column(db.Float, default=0.0)              # Qualidade dos registros
    energy_score = db.Column(db.Float, default=0.0)            # Eficiência energética
    
    # Score geral (média dos scores acima)
    overall_score = db.Column(db.Float, default=0.0)           # Nota final
    risk_level = db.Column(db.String(20), default='medium')    # baixo, médio, alto
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_overall_score(self):
        """Calcula a nota geral baseada nos scores individuais"""
        scores = [self.bias_score, self.transparency_score, self.logs_score, self.energy_score]
        valid_scores = [s for s in scores if s is not None]
        
        if valid_scores:
            self.overall_score = sum(valid_scores) / len(valid_scores)
        else:
            self.overall_score = 0.0
            
        # Determina o nível de risco baseado na nota
        if self.overall_score >= 80:
            self.risk_level = 'low'      # Verde - Baixo risco
        elif self.overall_score >= 60:
            self.risk_level = 'medium'   # Amarelo - Médio risco  
        else:
            self.risk_level = 'high'     # Vermelho - Alto risco
    
    def to_dict(self):
        """Converte os dados para um formato que o frontend pode usar"""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'system_name': self.system_name,
            'bias_score': self.bias_score,
            'transparency_score': self.transparency_score,
            'logs_score': self.logs_score,
            'energy_score': self.energy_score,
            'overall_score': self.overall_score,
            'risk_level': self.risk_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ComplianceAlert(db.Model):
    """
    Modelo para alertas de compliance
    Quando algo está fora do padrão, criamos um alerta
    """
    __tablename__ = 'compliance_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), nullable=False)
    system_name = db.Column(db.String(200), nullable=False)
    
    # Informações do alerta
    alert_type = db.Column(db.String(50), nullable=False)       # bias, transparency, etc.
    severity = db.Column(db.String(20), default='medium')       # low, medium, high, critical
    title = db.Column(db.String(200), nullable=False)           # Título do alerta
    description = db.Column(db.Text)                            # Descrição detalhada
    
    # Status
    status = db.Column(db.String(20), default='active')         # active, resolved, ignored
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.String(100))
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte os dados para um formato que o frontend pode usar"""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'system_name': self.system_name,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ComplianceReport(db.Model):
    """
    Modelo para relatórios de compliance
    Armazena relatórios gerados automaticamente
    """
    __tablename__ = 'compliance_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(100), nullable=False)
    
    # Informações do relatório
    report_type = db.Column(db.String(50), nullable=False)      # ai_act, gdpr, custom
    title = db.Column(db.String(200), nullable=False)
    period_start = db.Column(db.DateTime, nullable=False)       # Período do relatório
    period_end = db.Column(db.DateTime, nullable=False)
    
    # Conteúdo
    summary = db.Column(db.Text)                                # Resumo executivo
    findings = db.Column(db.Text)                               # Principais descobertas
    recommendations = db.Column(db.Text)                        # Recomendações
    
    # Arquivos
    pdf_path = db.Column(db.String(500))                        # Caminho do PDF
    json_data = db.Column(db.Text)                              # Dados em JSON
    
    # Status
    status = db.Column(db.String(20), default='draft')          # draft, final, archived
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    generated_by = db.Column(db.String(100))
    
    def to_dict(self):
        """Converte os dados para um formato que o frontend pode usar"""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'report_type': self.report_type,
            'title': self.title,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'summary': self.summary,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'pdf_path': self.pdf_path,
            'json_data': json.loads(self.json_data) if self.json_data else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'generated_by': self.generated_by
        }

