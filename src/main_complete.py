#!/usr/bin/env python3
"""
ZenThera AI Compliance Suite - Complete Version
Professional SaaS platform for AI compliance and governance
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import uuid
import random

app = Flask(__name__)
CORS(app)

# Configuração
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Criar diretório de upload
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Estado da aplicação
app_state = {
    'uploaded_files': [],
    'llm_connections': {},
    'current_connection': None,
    'regulation_sync': {
        'monitored_sources': 13,
        'last_update': '2025-07-19 21:33',
        'alerts_generated': 13,
        'status': 'active'
    },
    'predictive_compliance': {
        'risk_score': 0.23,
        'trend': 'improving',
        'last_analysis': '2025-07-19 21:30'
    },
    'ethical_ai_score': {
        'overall_score': 87.4,
        'percentile': 85,
        'last_calculated': '2025-07-19 21:25'
    }
}

# Template base
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - ZenThera AI Compliance Suite</title>
    <style>
        :root {
            --primary-color: #6366f1;
            --primary-light: #818cf8;
            --primary-dark: #4f46e5;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-400: #9ca3af;
            --gray-500: #6b7280;
            --gray-600: #4b5563;
            --gray-700: #374151;
            --gray-800: #1f2937;
            --gray-900: #111827;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--gray-50);
            color: var(--gray-900);
            line-height: 1.6;
        }

        .header {
            background: white;
            border-bottom: 1px solid var(--gray-200);
            padding: 0 24px;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 64px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 700;
            color: var(--primary-color);
            text-decoration: none;
        }

        .nav {
            display: flex;
            gap: 8px;
        }

        .nav-item {
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            color: var(--gray-600);
            font-weight: 500;
            transition: all 0.2s;
        }

        .nav-item:hover {
            background: var(--gray-100);
            color: var(--gray-900);
        }

        .nav-item.active {
            background: var(--primary-color);
            color: white;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }

        .page-header {
            margin-bottom: 32px;
        }

        .page-title {
            font-size: 32px;
            font-weight: 700;
            color: var(--gray-900);
            margin-bottom: 8px;
        }

        .page-subtitle {
            font-size: 16px;
            color: var(--gray-600);
        }

        .feature-status-banner {
            background: linear-gradient(135deg, var(--success-color), #059669);
            color: white;
            padding: 20px 24px;
            border-radius: 12px;
            margin-bottom: 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .feature-status-banner.partial {
            background: linear-gradient(135deg, var(--warning-color), #d97706);
        }

        .content-grid {
            display: grid;
            gap: 24px;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        }

        .content-card {
            background: white;
            border-radius: 12px;
            border: 1px solid var(--gray-200);
            overflow: hidden;
        }

        .card-header {
            padding: 24px 24px 0;
        }

        .card-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--gray-900);
            margin-bottom: 4px;
        }

        .card-subtitle {
            font-size: 14px;
            color: var(--gray-600);
        }

        .card-content {
            padding: 24px;
        }

        .metrics-grid {
            display: grid;
            gap: 16px;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        }

        .metric-card {
            background: var(--gray-50);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 4px;
        }

        .metric-label {
            font-size: 14px;
            color: var(--gray-600);
        }

        .alert {
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }

        .alert.success {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            color: #065f46;
        }

        .alert.warning {
            background: #fffbeb;
            border: 1px solid #fde68a;
            color: #92400e;
        }

        .alert.info {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1e40af;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 500;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--primary-color);
            color: white;
        }

        .btn-primary:hover {
            background: var(--primary-dark);
        }

        .upload-area {
            border: 2px dashed var(--gray-300);
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .upload-area:hover {
            border-color: var(--primary-color);
            background: var(--gray-50);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            display: block;
            font-weight: 500;
            margin-bottom: 8px;
            color: var(--gray-700);
        }

        .form-input, .form-select {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--gray-300);
            border-radius: 8px;
            font-size: 14px;
        }

        .form-input:focus, .form-select:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        @media (max-width: 768px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            .header-content {
                padding: 0 16px;
            }
            
            .container {
                padding: 16px;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="/" class="logo">
                <span>🛡️</span>
                <span>ZenThera</span>
            </a>
            <nav class="nav">
                <a href="/" class="nav-item {{ 'active' if page == 'dashboard' else '' }}">Dashboard</a>
                <a href="/setup" class="nav-item {{ 'active' if page == 'setup' else '' }}">Setup</a>
            </nav>
        </div>
    </header>

    <main class="container">
        {{ content|safe }}
    </main>

    <script>
        // Auto-refresh dashboard data
        if (window.location.pathname === '/') {
            setInterval(() => {
                fetch('/api/dashboard-data')
                    .then(response => response.json())
                    .then(data => {
                        // Update metrics if elements exist
                        const complianceScore = document.querySelector('[data-metric="compliance-score"]');
                        if (complianceScore) {
                            complianceScore.textContent = data.compliance_data.overall_score + '%';
                        }
                    })
                    .catch(console.error);
            }, 30000);
        }

        // Upload functionality
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        
        if (uploadArea && fileInput) {
            uploadArea.addEventListener('click', () => fileInput.click());
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = 'var(--primary-color)';
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.style.borderColor = 'var(--gray-300)';
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = 'var(--gray-300)';
                handleFiles(e.dataTransfer.files);
            });
            
            fileInput.addEventListener('change', (e) => {
                handleFiles(e.target.files);
            });
        }

        function handleFiles(files) {
            const formData = new FormData();
            for (let file of files) {
                formData.append('files', file);
            }
            
            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Upload error:', error);
                alert('Upload failed');
            });
        }

        // LLM Configuration
        const llmForm = document.getElementById('llm-config-form');
        const providerSelect = document.getElementById('llm-provider');
        const customEndpoint = document.getElementById('custom-endpoint');
        
        if (providerSelect && customEndpoint) {
            providerSelect.addEventListener('change', (e) => {
                customEndpoint.style.display = e.target.value === 'custom' ? 'block' : 'none';
            });
        }
        
        if (llmForm) {
            llmForm.addEventListener('submit', (e) => {
                e.preventDefault();
                
                const formData = new FormData(llmForm);
                const data = Object.fromEntries(formData.entries());
                
                fetch('/api/connect-llm', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Connection error:', error);
                    alert('Connection failed');
                });
            });
        }
    </script>
</body>
</html>
"""

def calculate_feature_status():
    """Calcula quantas features estão ativas"""
    active = 3  # Sempre ativas: Regulation Sync, Predictive Compliance, Ethical AI Score
    
    # Features que dependem de documentos
    if len(app_state['uploaded_files']) > 0:
        active += 3  # Compliance Grid, Bias Tracker, Testing Sandbox
    
    # Features que dependem de LLM
    if app_state['current_connection']:
        active += 1  # LLM Observability, Explainability, Failure Detection (contando como 1 para simplificar)
    
    return active

def generate_compliance_data():
    """Gera dados de compliance"""
    return {
        'overall_score': 72.9,
        'frameworks': {
            'eu_ai_act': {'score': 68.5, 'status': 'needs_attention'},
            'gdpr': {'score': 89.2, 'status': 'compliant'},
            'iso_27001': {'score': 71.8, 'status': 'needs_attention'},
            'soc2': {'score': 62.1, 'status': 'needs_attention'}
        }
    }

@app.route('/')
def dashboard():
    """Dashboard principal"""
    
    active_features = calculate_feature_status()
    compliance_data = generate_compliance_data()
    
    content = f"""
    <div class="page-header">
        <h1 class="page-title">AI Compliance Dashboard</h1>
        <p class="page-subtitle">Monitor your AI systems compliance and governance in real-time</p>
    </div>

    <!-- Status Banner -->
    <div class="feature-status-banner {'partial' if active_features < 7 else ''}">
        <div>
            <strong>{active_features}/7 Features Active</strong>
            <div style="font-size: 14px; opacity: 0.9;">
                {'Complete setup to unlock all compliance monitoring features' if active_features < 7 else 'All features active - comprehensive compliance monitoring enabled'}
            </div>
        </div>
        <div style="font-size: 24px;">
            {round((active_features / 7) * 100)}%
        </div>
    </div>

    <!-- Main Metrics -->
    <div class="content-grid">
        
        <!-- Compliance Overview -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">📊 Compliance Overview</h3>
                <p class="card-subtitle">Current compliance status across frameworks</p>
            </div>
            <div class="card-content">
                <div class="metric-card" style="margin-bottom: 20px;">
                    <div class="metric-value" data-metric="compliance-score">{compliance_data['overall_score']}%</div>
                    <div class="metric-label">Overall Compliance Score</div>
                </div>
                
                <div style="display: grid; gap: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                        <span>🇪🇺 EU AI Act</span>
                        <span style="font-weight: 600; color: var(--warning-color);">{compliance_data['frameworks']['eu_ai_act']['score']}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                        <span>🔒 GDPR</span>
                        <span style="font-weight: 600; color: var(--success-color);">{compliance_data['frameworks']['gdpr']['score']}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                        <span>📋 ISO 27001</span>
                        <span style="font-weight: 600; color: var(--warning-color);">{compliance_data['frameworks']['iso_27001']['score']}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                        <span>🛡️ SOC2</span>
                        <span style="font-weight: 600; color: var(--warning-color);">{compliance_data['frameworks']['soc2']['score']}%</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Active Features -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">🚀 Active Features</h3>
                <p class="card-subtitle">ZenThera features currently monitoring your systems</p>
            </div>
            <div class="card-content">
                <div style="display: grid; gap: 12px;">
                    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--success-color); color: white; border-radius: 6px;">
                        <span>✅</span>
                        <span>📡 Regulation Sync Module</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--success-color); color: white; border-radius: 6px;">
                        <span>✅</span>
                        <span>🎯 Predictive Compliance Engine</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--success-color); color: white; border-radius: 6px;">
                        <span>✅</span>
                        <span>⭐ Ethical AI Score</span>
                    </div>
                    
                    {'<div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--success-color); color: white; border-radius: 6px;"><span>✅</span><span>📊 Compliance Grid</span></div><div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--success-color); color: white; border-radius: 6px;"><span>✅</span><span>⚖️ Bias & Dataset Tracker</span></div><div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--success-color); color: white; border-radius: 6px;"><span>✅</span><span>🧪 Synthetic Testing Sandbox</span></div>' if len(app_state['uploaded_files']) > 0 else '<div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--gray-300); color: var(--gray-600); border-radius: 6px;"><span>⏸️</span><span>📊 Compliance Grid (Upload docs to activate)</span></div><div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--gray-300); color: var(--gray-600); border-radius: 6px;"><span>⏸️</span><span>⚖️ Bias Tracker (Upload docs to activate)</span></div><div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--gray-300); color: var(--gray-600); border-radius: 6px;"><span>⏸️</span><span>🧪 Testing Sandbox (Upload docs to activate)</span></div>'}
                    
                    {'<div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--success-color); color: white; border-radius: 6px;"><span>✅</span><span>🔍 LLM Observability Engine</span></div>' if app_state['current_connection'] else '<div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--gray-300); color: var(--gray-600); border-radius: 6px;"><span>⏸️</span><span>🔍 LLM Observability (Connect LLM to activate)</span></div>'}
                </div>
                
                {'<div class="alert success" style="margin-top: 16px;">All features active! Your compliance monitoring is comprehensive.</div>' if active_features == 7 else f'<div class="alert warning" style="margin-top: 16px;"><a href="/setup" style="color: var(--warning-color); text-decoration: underline;">Complete setup</a> to activate {7 - active_features} additional features.</div>'}
            </div>
        </div>

        <!-- System Status -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">📈 System Status</h3>
                <p class="card-subtitle">Real-time monitoring metrics</p>
            </div>
            <div class="card-content">
                <div class="metrics-grid" style="grid-template-columns: repeat(2, 1fr);">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: var(--primary-color);">{app_state['regulation_sync']['monitored_sources']}</div>
                        <div style="font-size: 12px; color: var(--gray-600);">Regulatory Sources</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: var(--success-color);">{len(app_state['uploaded_files'])}</div>
                        <div style="font-size: 12px; color: var(--gray-600);">Documents Uploaded</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: {'var(--success-color)' if app_state['current_connection'] else 'var(--gray-400)'};">{'✓' if app_state['current_connection'] else '○'}</div>
                        <div style="font-size: 12px; color: var(--gray-600);">LLM Connected</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: var(--warning-color);">{app_state['ethical_ai_score']['overall_score']}</div>
                        <div style="font-size: 12px; color: var(--gray-600);">Ethical AI Score</div>
                    </div>
                </div>
                
                <div style="margin-top: 20px; padding: 16px; background: var(--gray-50); border-radius: 8px;">
                    <div style="font-size: 14px; color: var(--gray-600); margin-bottom: 8px;">Last Updated</div>
                    <div style="font-size: 12px; color: var(--gray-500);">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">⚡ Quick Actions</h3>
                <p class="card-subtitle">Common tasks and next steps</p>
            </div>
            <div class="card-content">
                <div style="display: grid; gap: 12px;">
                    <a href="/setup" class="btn btn-primary">
                        <span>⚙️</span>
                        <span>Complete Setup</span>
                    </a>
                    
                    {'<button class="btn" style="background: var(--gray-100); color: var(--gray-600);" disabled><span>📄</span><span>Upload Documents (Complete)</span></button>' if len(app_state['uploaded_files']) > 0 else '<a href="/setup" class="btn" style="background: var(--warning-color); color: white;"><span>📄</span><span>Upload Documents</span></a>'}
                    
                    {'<button class="btn" style="background: var(--gray-100); color: var(--gray-600);" disabled><span>🤖</span><span>LLM Connected</span></button>' if app_state['current_connection'] else '<a href="/setup" class="btn" style="background: var(--primary-color); color: white;"><span>🤖</span><span>Connect LLM</span></a>'}
                    
                    <button class="btn" style="background: var(--gray-100); color: var(--gray-600);" onclick="location.reload()">
                        <span>🔄</span>
                        <span>Refresh Data</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
    """
    
    return render_template_string(BASE_TEMPLATE, 
                                title="Dashboard", 
                                content=content, 
                                page="dashboard")

@app.route('/setup')
def setup_page():
    """Página de configuração e setup"""
    
    active_features = calculate_feature_status()
    
    content = f"""
    <div class="page-header">
        <h1 class="page-title">Setup & Configuration</h1>
        <p class="page-subtitle">Configure your ZenThera AI Compliance Suite for maximum coverage</p>
    </div>

    <!-- Setup Progress -->
    <div class="feature-status-banner {'partial' if active_features < 7 else ''}">
        <div>
            <strong>Setup Progress: {active_features}/7 Features Active</strong>
            <div style="font-size: 14px; opacity: 0.9;">
                {'Complete all steps below to unlock full compliance monitoring' if active_features < 7 else 'All features active - your compliance suite is ready!'}
            </div>
        </div>
        <div style="font-size: 24px;">
            {round((active_features / 7) * 100)}%
        </div>
    </div>

    <!-- Setup Steps -->
    <div class="content-grid">
        
        <!-- Step 1: Always Active Features -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">✅ Step 1: Independent Features</h3>
                <p class="card-subtitle">These features are always active and require no setup</p>
            </div>
            <div class="card-content">
                <div class="alert success">
                    <strong>3/3 Features Active</strong><br>
                    Regulation Sync, Predictive Compliance, and Ethical AI Score are monitoring your compliance automatically.
                </div>
                
                <div style="margin-top: 16px;">
                    <h4 style="margin-bottom: 12px;">Active Features:</h4>
                    <ul style="margin-left: 20px; color: var(--gray-600);">
                        <li><strong>📡 Regulation Sync Module</strong> - Monitoring {app_state['regulation_sync']['monitored_sources']} regulatory sources</li>
                        <li><strong>🎯 Predictive Compliance</strong> - Risk score: {app_state['predictive_compliance']['risk_score']}</li>
                        <li><strong>⭐ Ethical AI Score</strong> - Current score: {app_state['ethical_ai_score']['overall_score']}</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Step 2: Document Upload -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">📋 Step 2: Upload Compliance Documents</h3>
                <p class="card-subtitle">Upload regulatory documents to activate 3 additional features</p>
            </div>
            <div class="card-content">
                
                {'<div class="alert success"><strong>Documents uploaded!</strong> Compliance Grid, Bias Tracker, and Testing Sandbox are now active.</div>' if len(app_state['uploaded_files']) > 0 else '<div class="alert warning"><strong>No documents uploaded yet.</strong> Upload compliance documents to activate additional features.</div>'}
                
                <!-- Upload Area -->
                <div class="upload-area" id="upload-area" style="margin: 20px 0;">
                    <div style="font-size: 48px; margin-bottom: 16px;">📁</div>
                    <h4>Drag & Drop Files Here</h4>
                    <p style="color: var(--gray-500); margin: 8px 0;">or click to browse</p>
                    <p style="font-size: 12px; color: var(--gray-400);">
                        Supported: PDF, DOC, DOCX, TXT, JSON, CSV, MD, XML, YAML (max 50MB)
                    </p>
                    <input type="file" id="file-input" multiple accept=".pdf,.doc,.docx,.txt,.json,.csv,.md,.xml,.yaml,.yml" style="display: none;">
                </div>

                <!-- Uploaded Files -->
                {'<div style="margin-top: 20px;"><h4>Uploaded Files (' + str(len(app_state['uploaded_files'])) + '):</h4>' + ''.join([f'<div style="padding: 8px; background: var(--gray-50); border-radius: 6px; margin: 4px 0; display: flex; justify-content: space-between; align-items: center;"><span>📄 {file["name"]}</span><span style="font-size: 12px; color: var(--gray-500);">{file["size"]}</span></div>' for file in app_state['uploaded_files']]) + '</div>' if len(app_state['uploaded_files']) > 0 else ''}
            </div>
        </div>

        <!-- Step 3: LLM Integration -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">🤖 Step 3: Connect Your LLM (Optional)</h3>
                <p class="card-subtitle">Connect your LLM for real-time monitoring and advanced features</p>
            </div>
            <div class="card-content">
                
                {'<div class="alert success"><strong>LLM Connected!</strong> Observability, Explainability, and Failure Detection are now active.</div>' if app_state['current_connection'] else '<div class="alert info"><strong>Optional Step:</strong> Connect your LLM for advanced monitoring features.</div>'}

                <!-- LLM Configuration Form -->
                <form id="llm-config-form" style="margin-top: 20px;">
                    <div class="form-group">
                        <label class="form-label">LLM Provider</label>
                        <select class="form-select" id="llm-provider" name="provider">
                            <option value="">Select Provider</option>
                            <option value="openai">OpenAI (GPT-4, GPT-3.5)</option>
                            <option value="anthropic">Anthropic (Claude)</option>
                            <option value="azure">Azure OpenAI</option>
                            <option value="google">Google (Gemini)</option>
                            <option value="custom">Custom API</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">API Key</label>
                        <input type="password" class="form-input" id="api-key" name="api_key" placeholder="sk-..." />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Model Name</label>
                        <input type="text" class="form-input" id="model-name" name="model" placeholder="gpt-4, claude-3-sonnet, etc." />
                    </div>
                    
                    <div class="form-group" id="custom-endpoint" style="display: none;">
                        <label class="form-label">Custom Endpoint URL</label>
                        <input type="url" class="form-input" id="endpoint-url" name="endpoint" placeholder="https://api.yourcompany.com/v1" />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Integration Method</label>
                        <select class="form-select" id="integration-method" name="method">
                            <option value="sdk">SDK Integration (Recommended)</option>
                            <option value="webhook">Webhook (Post-execution)</option>
                            <option value="batch">Batch Upload (Restricted environments)</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">
                        <span>🔗</span>
                        <span>Connect LLM</span>
                    </button>
                </form>
            </div>
        </div>

        <!-- Setup Summary -->
        <div class="content-card">
            <div class="card-header">
                <h3 class="card-title">📊 Setup Summary</h3>
                <p class="card-subtitle">Your current ZenThera configuration</p>
            </div>
            <div class="card-content">
                <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));">
                    <div style="text-align: center; padding: 16px;">
                        <div style="font-size: 32px; font-weight: 700; color: var(--success-color);">{active_features}</div>
                        <div style="font-size: 14px; color: var(--gray-600);">Active Features</div>
                    </div>
                    <div style="text-align: center; padding: 16px;">
                        <div style="font-size: 32px; font-weight: 700; color: var(--primary-color);">{len(app_state['uploaded_files'])}</div>
                        <div style="font-size: 14px; color: var(--gray-600);">Documents</div>
                    </div>
                    <div style="text-align: center; padding: 16px;">
                        <div style="font-size: 32px; font-weight: 700; color: {'var(--success-color)' if app_state['current_connection'] else 'var(--gray-400)'};">{'✓' if app_state['current_connection'] else '○'}</div>
                        <div style="font-size: 14px; color: var(--gray-600);">LLM Status</div>
                    </div>
                    <div style="text-align: center; padding: 16px;">
                        <div style="font-size: 32px; font-weight: 700; color: var(--warning-color);">{round((active_features / 7) * 100)}%</div>
                        <div style="font-size: 14px; color: var(--gray-600);">Complete</div>
                    </div>
                </div>

                <!-- Next Steps -->
                <div style="margin-top: 24px;">
                    {'<div class="alert success">🎉 Setup complete! All features are active. <a href="/" style="color: var(--primary-color); text-decoration: underline;">Go to Dashboard</a></div>' if active_features == 7 else f'<div class="alert warning">Complete the remaining steps to unlock all {7 - active_features} features.</div>'}
                </div>
            </div>
        </div>
    </div>
    """
    
    return render_template_string(BASE_TEMPLATE, 
                                title="Setup & Configuration", 
                                content=content, 
                                page="setup")

# APIs
@app.route('/api/upload', methods=['POST'])
def upload_files():
    """API para upload de arquivos"""
    try:
        if 'files' not in request.files:
            return jsonify({'status': 'error', 'message': 'No files provided'})
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        for file in files:
            if file and file.filename:
                # Simular upload (não salvar arquivo real para demo)
                file_info = {
                    'name': file.filename,
                    'size': f"{random.randint(50, 500)} KB",
                    'uploaded_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'type': file.filename.split('.')[-1].upper() if '.' in file.filename else 'Unknown'
                }
                
                app_state['uploaded_files'].append(file_info)
                uploaded_files.append(file_info)
        
        return jsonify({
            'status': 'success',
            'message': f'{len(uploaded_files)} files uploaded successfully',
            'files': uploaded_files,
            'total_files': len(app_state['uploaded_files'])
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/connect-llm', methods=['POST'])
def connect_llm():
    """API para conectar LLM"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['provider', 'api_key', 'model', 'method']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'})
        
        # Criar conexão
        connection_id = str(uuid.uuid4())
        connection_info = {
            'id': connection_id,
            'provider': data['provider'],
            'model': data['model'],
            'method': data['method'],
            'endpoint': data.get('endpoint', ''),
            'connected_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'status': 'active'
        }
        
        # Salvar conexão
        app_state['llm_connections'][connection_id] = connection_info
        app_state['current_connection'] = connection_id
        
        return jsonify({
            'status': 'success',
            'message': 'LLM connected successfully',
            'connection': connection_info
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/dashboard-data')
def dashboard_data():
    """API para dados do dashboard"""
    return jsonify({
        'compliance_data': generate_compliance_data(),
        'active_features': calculate_feature_status(),
        'regulation_sync': app_state['regulation_sync'],
        'uploaded_files': len(app_state['uploaded_files']),
        'llm_connected': bool(app_state['current_connection']),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ZenThera AI Compliance Suite',
        'version': '1.0.0',
        'features_active': calculate_feature_status(),
        'total_features': 7,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("🚀 Starting ZenThera AI Compliance Suite...")
    print("📊 Dashboard: http://localhost:5015/")
    print("⚙️ Setup: http://localhost:5015/setup")
    print("🔗 Health: http://localhost:5015/api/health")
    app.run(host='0.0.0.0', port=5015, debug=True)

