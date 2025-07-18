"""
ZenThera Compliance Grid - API Routes
Este arquivo define as rotas (endpoints) da API para o sistema de compliance
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.compliance import ComplianceScore, ComplianceAlert, ComplianceReport, db
import json

# Criar blueprint para organizar as rotas
compliance_bp = Blueprint('compliance', __name__)

# ============================================================================
# DASHBOARD ENDPOINTS - Dados principais para o painel de controle
# ============================================================================

@compliance_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """
    Endpoint principal do dashboard
    Retorna dados resumidos de compliance para a organização
    """
    try:
        # Pegar parâmetros da URL
        org_id = request.args.get('org_id', 'default_org')
        
        # Buscar score mais recente da organização
        latest_score = ComplianceScore.query.filter_by(
            organization_id=org_id
        ).order_by(ComplianceScore.updated_at.desc()).first()
        
        # Buscar alertas ativos
        active_alerts = ComplianceAlert.query.filter_by(
            organization_id=org_id,
            status='active'
        ).all()
        
        # Contar alertas por severidade
        alert_counts = {
            'critical': len([a for a in active_alerts if a.severity == 'critical']),
            'high': len([a for a in active_alerts if a.severity == 'high']),
            'medium': len([a for a in active_alerts if a.severity == 'medium']),
            'low': len([a for a in active_alerts if a.severity == 'low'])
        }
        
        # Buscar histórico dos últimos 30 dias para gráfico de tendência
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        historical_scores = ComplianceScore.query.filter(
            ComplianceScore.organization_id == org_id,
            ComplianceScore.created_at >= thirty_days_ago
        ).order_by(ComplianceScore.created_at.asc()).all()
        
        # Preparar dados de tendência
        trend_data = []
        for score in historical_scores:
            trend_data.append({
                'date': score.created_at.strftime('%Y-%m-%d'),
                'overall_score': score.overall_score,
                'bias_score': score.bias_score,
                'transparency_score': score.transparency_score,
                'logs_score': score.logs_score,
                'energy_score': score.energy_score
            })
        
        # Montar resposta do dashboard
        dashboard_data = {
            'organization_id': org_id,
            'current_score': latest_score.to_dict() if latest_score else None,
            'alert_summary': {
                'total_active': len(active_alerts),
                'by_severity': alert_counts
            },
            'trend_data': trend_data,
            'last_updated': datetime.utcnow().isoformat(),
            'status': 'success'
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to load dashboard',
            'message': str(e),
            'status': 'error'
        }), 500

@compliance_bp.route('/score/<org_id>', methods=['GET'])
def get_compliance_score(org_id):
    """
    Buscar score de compliance específico de uma organização
    """
    try:
        # Buscar score mais recente
        score = ComplianceScore.query.filter_by(
            organization_id=org_id
        ).order_by(ComplianceScore.updated_at.desc()).first()
        
        if not score:
            return jsonify({
                'error': 'No compliance score found',
                'organization_id': org_id,
                'status': 'not_found'
            }), 404
        
        return jsonify({
            'score': score.to_dict(),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve score',
            'message': str(e),
            'status': 'error'
        }), 500

@compliance_bp.route('/score', methods=['POST'])
def create_compliance_score():
    """
    Criar ou atualizar score de compliance
    Usado quando um sistema de IA é analisado
    """
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['organization_id', 'system_name']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'validation_error'
                }), 400
        
        # Criar novo score
        score = ComplianceScore(
            organization_id=data['organization_id'],
            system_name=data['system_name'],
            bias_score=data.get('bias_score', 0.0),
            transparency_score=data.get('transparency_score', 0.0),
            logs_score=data.get('logs_score', 0.0),
            energy_score=data.get('energy_score', 0.0)
        )
        
        # Calcular score geral automaticamente
        score.calculate_overall_score()
        
        # Salvar no banco de dados
        db.session.add(score)
        db.session.commit()
        
        # Verificar se precisa criar alertas
        check_and_create_alerts(score)
        
        return jsonify({
            'score': score.to_dict(),
            'message': 'Compliance score created successfully',
            'status': 'success'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create score',
            'message': str(e),
            'status': 'error'
        }), 500

# ============================================================================
# ALERTS ENDPOINTS - Gerenciamento de alertas de compliance
# ============================================================================

@compliance_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """
    Listar alertas de compliance
    Suporta filtros por organização, status, severidade
    """
    try:
        # Pegar parâmetros de filtro
        org_id = request.args.get('org_id')
        status = request.args.get('status', 'active')
        severity = request.args.get('severity')
        limit = int(request.args.get('limit', 50))
        
        # Construir query
        query = ComplianceAlert.query
        
        if org_id:
            query = query.filter_by(organization_id=org_id)
        
        if status:
            query = query.filter_by(status=status)
            
        if severity:
            query = query.filter_by(severity=severity)
        
        # Ordenar por data de criação (mais recentes primeiro)
        alerts = query.order_by(
            ComplianceAlert.created_at.desc()
        ).limit(limit).all()
        
        return jsonify({
            'alerts': [alert.to_dict() for alert in alerts],
            'total': len(alerts),
            'filters': {
                'org_id': org_id,
                'status': status,
                'severity': severity,
                'limit': limit
            },
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve alerts',
            'message': str(e),
            'status': 'error'
        }), 500

@compliance_bp.route('/alerts', methods=['POST'])
def create_alert():
    """
    Criar novo alerta de compliance
    """
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['organization_id', 'system_name', 'alert_type', 'title']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'validation_error'
                }), 400
        
        # Criar novo alerta
        alert = ComplianceAlert(
            organization_id=data['organization_id'],
            system_name=data['system_name'],
            alert_type=data['alert_type'],
            severity=data.get('severity', 'medium'),
            title=data['title'],
            description=data.get('description', ''),
            status='active'
        )
        
        # Salvar no banco de dados
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            'alert': alert.to_dict(),
            'message': 'Alert created successfully',
            'status': 'success'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create alert',
            'message': str(e),
            'status': 'error'
        }), 500

@compliance_bp.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """
    Atualizar status de um alerta
    """
    try:
        alert = ComplianceAlert.query.get(alert_id)
        
        if not alert:
            return jsonify({
                'error': 'Alert not found',
                'alert_id': alert_id,
                'status': 'not_found'
            }), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'status' in data:
            alert.status = data['status']
            if data['status'] == 'resolved':
                alert.resolved_at = datetime.utcnow()
                alert.resolved_by = data.get('resolved_by', 'system')
        
        if 'severity' in data:
            alert.severity = data['severity']
        
        # Salvar mudanças
        db.session.commit()
        
        return jsonify({
            'alert': alert.to_dict(),
            'message': 'Alert updated successfully',
            'status': 'success'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update alert',
            'message': str(e),
            'status': 'error'
        }), 500

# ============================================================================
# REPORTS ENDPOINTS - Geração e gerenciamento de relatórios
# ============================================================================

@compliance_bp.route('/reports', methods=['GET'])
def get_reports():
    """
    Listar relatórios de compliance
    """
    try:
        org_id = request.args.get('org_id')
        report_type = request.args.get('type')
        limit = int(request.args.get('limit', 20))
        
        # Construir query
        query = ComplianceReport.query
        
        if org_id:
            query = query.filter_by(organization_id=org_id)
            
        if report_type:
            query = query.filter_by(report_type=report_type)
        
        # Ordenar por data de criação (mais recentes primeiro)
        reports = query.order_by(
            ComplianceReport.created_at.desc()
        ).limit(limit).all()
        
        return jsonify({
            'reports': [report.to_dict() for report in reports],
            'total': len(reports),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve reports',
            'message': str(e),
            'status': 'error'
        }), 500

@compliance_bp.route('/reports/generate', methods=['POST'])
def generate_report():
    """
    Gerar novo relatório de compliance
    """
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['organization_id', 'report_type', 'period_start', 'period_end']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'validation_error'
                }), 400
        
        # Converter datas
        period_start = datetime.fromisoformat(data['period_start'].replace('Z', '+00:00'))
        period_end = datetime.fromisoformat(data['period_end'].replace('Z', '+00:00'))
        
        # Gerar conteúdo do relatório
        report_content = generate_report_content(
            data['organization_id'],
            data['report_type'],
            period_start,
            period_end
        )
        
        # Criar relatório
        report = ComplianceReport(
            organization_id=data['organization_id'],
            report_type=data['report_type'],
            title=data.get('title', f"{data['report_type'].upper()} Compliance Report"),
            period_start=period_start,
            period_end=period_end,
            summary=report_content['summary'],
            findings=report_content['findings'],
            recommendations=report_content['recommendations'],
            json_data=json.dumps(report_content['data']),
            status='final',
            generated_by='system'
        )
        
        # Salvar no banco de dados
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'report': report.to_dict(),
            'message': 'Report generated successfully',
            'status': 'success'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to generate report',
            'message': str(e),
            'status': 'error'
        }), 500

# ============================================================================
# HELPER FUNCTIONS - Funções auxiliares
# ============================================================================

def check_and_create_alerts(score):
    """
    Verificar se um score precisa gerar alertas automáticos
    """
    try:
        # Alerta para score geral baixo
        if score.overall_score < 60:
            severity = 'critical' if score.overall_score < 40 else 'high'
            
            alert = ComplianceAlert(
                organization_id=score.organization_id,
                system_name=score.system_name,
                alert_type='low_compliance_score',
                severity=severity,
                title=f'Low Compliance Score: {score.overall_score}%',
                description=f'System {score.system_name} has a compliance score of {score.overall_score}%, which is below the acceptable threshold.',
                status='active'
            )
            
            db.session.add(alert)
        
        # Alertas específicos por métrica
        metrics = [
            ('bias_score', 'bias_violation', 'High Bias Risk'),
            ('transparency_score', 'transparency_issue', 'Low Transparency'),
            ('logs_score', 'logging_deficiency', 'Inadequate Logging'),
            ('energy_score', 'energy_inefficiency', 'High Energy Consumption')
        ]
        
        for metric_name, alert_type, title_prefix in metrics:
            metric_value = getattr(score, metric_name)
            if metric_value < 50:
                severity = 'high' if metric_value < 30 else 'medium'
                
                alert = ComplianceAlert(
                    organization_id=score.organization_id,
                    system_name=score.system_name,
                    alert_type=alert_type,
                    severity=severity,
                    title=f'{title_prefix}: {metric_value}%',
                    description=f'{metric_name.replace("_", " ").title()} is {metric_value}%, indicating potential compliance issues.',
                    status='active'
                )
                
                db.session.add(alert)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Error creating alerts: {e}")
        db.session.rollback()

def generate_report_content(org_id, report_type, period_start, period_end):
    """
    Gerar conteúdo do relatório baseado nos dados de compliance
    """
    try:
        # Buscar dados do período
        scores = ComplianceScore.query.filter(
            ComplianceScore.organization_id == org_id,
            ComplianceScore.created_at >= period_start,
            ComplianceScore.created_at <= period_end
        ).all()
        
        alerts = ComplianceAlert.query.filter(
            ComplianceAlert.organization_id == org_id,
            ComplianceAlert.created_at >= period_start,
            ComplianceAlert.created_at <= period_end
        ).all()
        
        # Calcular estatísticas
        if scores:
            avg_score = sum(s.overall_score for s in scores) / len(scores)
            min_score = min(s.overall_score for s in scores)
            max_score = max(s.overall_score for s in scores)
        else:
            avg_score = min_score = max_score = 0
        
        # Contar alertas por severidade
        alert_counts = {
            'critical': len([a for a in alerts if a.severity == 'critical']),
            'high': len([a for a in alerts if a.severity == 'high']),
            'medium': len([a for a in alerts if a.severity == 'medium']),
            'low': len([a for a in alerts if a.severity == 'low'])
        }
        
        # Gerar conteúdo
        summary = f"""
        Executive Summary:
        During the period from {period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}, 
        the organization maintained an average compliance score of {avg_score:.1f}%.
        
        Key Metrics:
        - Average Compliance Score: {avg_score:.1f}%
        - Minimum Score: {min_score:.1f}%
        - Maximum Score: {max_score:.1f}%
        - Total Alerts Generated: {len(alerts)}
        """
        
        findings = f"""
        Key Findings:
        1. Compliance Performance: {'Good' if avg_score >= 80 else 'Needs Improvement' if avg_score >= 60 else 'Critical'}
        2. Alert Distribution: {alert_counts['critical']} critical, {alert_counts['high']} high, {alert_counts['medium']} medium, {alert_counts['low']} low
        3. Systems Monitored: {len(set(s.system_name for s in scores))}
        """
        
        recommendations = f"""
        Recommendations:
        1. {'Maintain current practices' if avg_score >= 80 else 'Improve compliance processes'}
        2. {'Monitor for any degradation' if avg_score >= 80 else 'Address critical alerts immediately'}
        3. Regular monitoring and assessment of AI systems
        """
        
        # Dados estruturados
        data = {
            'period': {
                'start': period_start.isoformat(),
                'end': period_end.isoformat()
            },
            'statistics': {
                'average_score': avg_score,
                'minimum_score': min_score,
                'maximum_score': max_score,
                'total_assessments': len(scores),
                'total_alerts': len(alerts)
            },
            'alert_breakdown': alert_counts,
            'scores': [s.to_dict() for s in scores],
            'alerts': [a.to_dict() for a in alerts]
        }
        
        return {
            'summary': summary.strip(),
            'findings': findings.strip(),
            'recommendations': recommendations.strip(),
            'data': data
        }
        
    except Exception as e:
        return {
            'summary': f'Error generating report: {str(e)}',
            'findings': 'Unable to analyze data',
            'recommendations': 'Please check system configuration',
            'data': {}
        }

