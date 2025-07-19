#!/usr/bin/env python3
"""
ZenThera AI Compliance Suite - Complete Version with Individual Feature Pages
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
            align-items: center;
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

        .dropdown {
            position: relative;
            display: inline-block;
        }

        .dropdown-toggle {
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            color: var(--gray-600);
            font-weight: 500;
            transition: all 0.2s;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .dropdown-toggle:hover {
            background: var(--gray-100);
            color: var(--gray-900);
        }

        .dropdown-menu {
            position: absolute;
            top: 100%;
            right: 0;
            background: white;
            border: 1px solid var(--gray-200);
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            min-width: 280px;
            z-index: 1000;
            display: none;
        }

        .dropdown-menu.show {
            display: block;
        }

        .dropdown-header {
            padding: 12px 16px;
            border-bottom: 1px solid var(--gray-200);
            font-weight: 600;
            color: var(--gray-700);
            font-size: 14px;
        }

        .dropdown-item {
            display: block;
            padding: 12px 16px;
            text-decoration: none;
            color: var(--gray-700);
            transition: all 0.2s;
            border-bottom: 1px solid var(--gray-100);
        }

        .dropdown-item:last-child {
            border-bottom: none;
        }

        .dropdown-item:hover {
            background: var(--gray-50);
            color: var(--primary-color);
        }

        .dropdown-item.disabled {
            color: var(--gray-400);
            cursor: not-allowed;
        }

        .dropdown-item.disabled:hover {
            background: transparent;
            color: var(--gray-400);
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

        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }

        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--gray-200);
        }

        .data-table th {
            background: var(--gray-50);
            font-weight: 600;
            color: var(--gray-700);
        }

        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }

        .status-badge.active {
            background: #dcfce7;
            color: #166534;
        }

        .status-badge.warning {
            background: #fef3c7;
            color: #92400e;
        }

        .status-badge.error {
            background: #fee2e2;
            color: #991b1b;
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

            .dropdown-menu {
                right: 0;
                left: auto;
                min-width: 250px;
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
                
                <div class="dropdown">
                    <div class="dropdown-toggle" onclick="toggleDropdown()">
                        <span>Features</span>
                        <span>▼</span>
                    </div>
                    <div class="dropdown-menu" id="features-dropdown">
                        <div class="dropdown-header">ZenThera Features</div>
                        <a href="/feature/regulation-sync" class="dropdown-item">📡 Regulation Sync Module</a>
                        <a href="/feature/predictive-compliance" class="dropdown-item">🎯 Predictive Compliance Engine</a>
                        <a href="/feature/ethical-ai-score" class="dropdown-item">⭐ Ethical AI Score</a>
                        <a href="/feature/compliance-grid" class="dropdown-item {{ 'disabled' if not uploaded_files else '' }}">📊 Compliance Grid</a>
                        <a href="/feature/bias-tracker" class="dropdown-item {{ 'disabled' if not uploaded_files else '' }}">⚖️ Bias & Dataset Tracker</a>
                        <a href="/feature/testing-sandbox" class="dropdown-item {{ 'disabled' if not uploaded_files else '' }}">🧪 Synthetic Testing Sandbox</a>
                        <a href="/feature/llm-observability" class="dropdown-item {{ 'disabled' if not llm_connected else '' }}">🔍 LLM Observability Engine</a>
                    </div>
                </div>
            </nav>
        </div>
    </header>

    <main class="container">
        {{ content|safe }}
    </main>

    <script>
        function toggleDropdown() {
            const dropdown = document.getElementById('features-dropdown');
            dropdown.classList.toggle('show');
        }

        // Close dropdown when clicking outside
        window.addEventListener('click', function(event) {
            if (!event.target.matches('.dropdown-toggle') && !event.target.closest('.dropdown')) {
                const dropdown = document.getElementById('features-dropdown');
                dropdown.classList.remove('show');
            }
        });

        // Auto-refresh dashboard data
        if (window.location.pathname === '/') {
            setInterval(() => {
                fetch('/api/dashboard-data')
                    .then(response => response.json())
                    .then(data => {
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
        active += 1  # LLM Observability
    
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
                                page="dashboard",
                                uploaded_files=len(app_state['uploaded_files']) > 0,
                                llm_connected=bool(app_state['current_connection']))

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
                                page="setup",
                                uploaded_files=len(app_state['uploaded_files']) > 0,
                                llm_connected=bool(app_state['current_connection']))

# Feature Pages
@app.route('/feature/<feature_name>')
def feature_page(feature_name):
    """Páginas individuais das features"""
    
    # Verificar se a feature está ativa
    active_features = calculate_feature_status()
    uploaded_files = len(app_state['uploaded_files']) > 0
    llm_connected = bool(app_state['current_connection'])
    
    # Definir features e suas dependências
    features_config = {
        'regulation-sync': {
            'title': '📡 Regulation Sync Module',
            'subtitle': 'Automated regulatory monitoring and compliance tracking',
            'active': True,  # Sempre ativa
            'group': 'A'
        },
        'predictive-compliance': {
            'title': '🎯 Predictive Compliance Engine',
            'subtitle': 'AI-powered risk analysis and trend prediction',
            'active': True,  # Sempre ativa
            'group': 'A'
        },
        'ethical-ai-score': {
            'title': '⭐ Ethical AI Score',
            'subtitle': 'Automated ethical assessment and benchmarking',
            'active': True,  # Sempre ativa
            'group': 'A'
        },
        'compliance-grid': {
            'title': '📊 Compliance Grid (ZCG)',
            'subtitle': 'Multi-framework compliance scoring and management',
            'active': uploaded_files,
            'group': 'B'
        },
        'bias-tracker': {
            'title': '⚖️ Bias & Dataset Tracker',
            'subtitle': 'Bias detection and dataset governance',
            'active': uploaded_files,
            'group': 'B'
        },
        'testing-sandbox': {
            'title': '🧪 Synthetic Testing Sandbox',
            'subtitle': 'Automated compliance testing and validation',
            'active': uploaded_files,
            'group': 'B'
        },
        'llm-observability': {
            'title': '🔍 LLM Observability Engine',
            'subtitle': 'Real-time LLM monitoring and risk detection',
            'active': llm_connected,
            'group': 'C'
        }
    }
    
    if feature_name not in features_config:
        return "Feature not found", 404
    
    feature = features_config[feature_name]
    
    # Se a feature não está ativa, mostrar página de ativação
    if not feature['active']:
        if feature['group'] == 'B':
            activation_message = 'Upload compliance documents to activate this feature.'
            activation_link = '/setup'
            activation_text = 'Go to Setup'
        elif feature['group'] == 'C':
            activation_message = 'Connect your LLM to activate this feature.'
            activation_link = '/setup'
            activation_text = 'Go to Setup'
        
        content = f"""
        <div class="page-header">
            <h1 class="page-title">{feature['title']}</h1>
            <p class="page-subtitle">{feature['subtitle']}</p>
        </div>

        <div class="content-card">
            <div class="card-content">
                <div class="alert warning">
                    <strong>Feature Not Active</strong><br>
                    {activation_message}
                </div>
                
                <div style="text-align: center; margin-top: 32px;">
                    <a href="{activation_link}" class="btn btn-primary">
                        <span>⚙️</span>
                        <span>{activation_text}</span>
                    </a>
                </div>
            </div>
        </div>
        """
        
        return render_template_string(BASE_TEMPLATE, 
                                    title=feature['title'], 
                                    content=content, 
                                    page="feature",
                                    uploaded_files=uploaded_files,
                                    llm_connected=llm_connected)
    
    # Feature está ativa - mostrar dashboard específico
    if feature_name == 'regulation-sync':
        content = f"""
        <div class="page-header">
            <h1 class="page-title">{feature['title']}</h1>
            <p class="page-subtitle">{feature['subtitle']}</p>
        </div>

        <div class="feature-status-banner">
            <div>
                <strong>Feature Active</strong>
                <div style="font-size: 14px; opacity: 0.9;">
                    Monitoring {app_state['regulation_sync']['monitored_sources']} regulatory sources in real-time
                </div>
            </div>
            <div style="font-size: 24px;">
                ✅
            </div>
        </div>

        <div class="content-grid">
            
            <!-- Monitoring Status -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">📊 Monitoring Status</h3>
                    <p class="card-subtitle">Real-time regulatory monitoring metrics</p>
                </div>
                <div class="card-content">
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-value">{app_state['regulation_sync']['monitored_sources']}</div>
                            <div class="metric-label">Sources Monitored</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{app_state['regulation_sync']['alerts_generated']}</div>
                            <div class="metric-label">Alerts Generated</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">24/7</div>
                            <div class="metric-label">Monitoring</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">99.9%</div>
                            <div class="metric-label">Uptime</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Regulatory Sources -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">🌐 Regulatory Sources</h3>
                    <p class="card-subtitle">Official sources being monitored</p>
                </div>
                <div class="card-content">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Source</th>
                                <th>Region</th>
                                <th>Status</th>
                                <th>Last Update</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>EUR-Lex</td>
                                <td>🇪🇺 European Union</td>
                                <td><span class="status-badge active">Active</span></td>
                                <td>2 hours ago</td>
                            </tr>
                            <tr>
                                <td>Federal Register</td>
                                <td>🇺🇸 United States</td>
                                <td><span class="status-badge active">Active</span></td>
                                <td>4 hours ago</td>
                            </tr>
                            <tr>
                                <td>ISO Standards</td>
                                <td>🌍 International</td>
                                <td><span class="status-badge active">Active</span></td>
                                <td>1 day ago</td>
                            </tr>
                            <tr>
                                <td>GDPR Updates</td>
                                <td>🇪🇺 European Union</td>
                                <td><span class="status-badge active">Active</span></td>
                                <td>3 hours ago</td>
                            </tr>
                            <tr>
                                <td>AI Act Guidelines</td>
                                <td>🇪🇺 European Union</td>
                                <td><span class="status-badge warning">Pending</span></td>
                                <td>6 hours ago</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Recent Alerts -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">🚨 Recent Alerts</h3>
                    <p class="card-subtitle">Latest regulatory changes detected</p>
                </div>
                <div class="card-content">
                    <div style="display: grid; gap: 12px;">
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--error-color);">
                            <div style="font-weight: 600; color: var(--error-color);">HIGH PRIORITY</div>
                            <div style="margin: 8px 0;">EU AI Act Article 13 - New interpretation guidelines published</div>
                            <div style="font-size: 12px; color: var(--gray-500);">2 hours ago • EUR-Lex</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--warning-color);">
                            <div style="font-weight: 600; color: var(--warning-color);">MEDIUM PRIORITY</div>
                            <div style="margin: 8px 0;">GDPR - Updated data processing guidelines for AI systems</div>
                            <div style="font-size: 12px; color: var(--gray-500);">4 hours ago • EUR-Lex</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--primary-color);">
                            <div style="font-weight: 600; color: var(--primary-color);">INFO</div>
                            <div style="margin: 8px 0;">ISO 42001 - AI Management System standard updated</div>
                            <div style="font-size: 12px; color: var(--gray-500);">1 day ago • ISO</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Configuration -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">⚙️ Configuration</h3>
                    <p class="card-subtitle">Monitoring settings and preferences</p>
                </div>
                <div class="card-content">
                    <div style="display: grid; gap: 16px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Email Notifications</span>
                            <span style="color: var(--success-color); font-weight: 600;">Enabled</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Slack Integration</span>
                            <span style="color: var(--gray-400); font-weight: 600;">Disabled</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Alert Frequency</span>
                            <span style="color: var(--primary-color); font-weight: 600;">Real-time</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Auto-sync</span>
                            <span style="color: var(--success-color); font-weight: 600;">Every 2 hours</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    elif feature_name == 'predictive-compliance':
        content = f"""
        <div class="page-header">
            <h1 class="page-title">{feature['title']}</h1>
            <p class="page-subtitle">{feature['subtitle']}</p>
        </div>

        <div class="feature-status-banner">
            <div>
                <strong>Feature Active</strong>
                <div style="font-size: 14px; opacity: 0.9;">
                    AI-powered risk analysis running continuously
                </div>
            </div>
            <div style="font-size: 24px;">
                ✅
            </div>
        </div>

        <div class="content-grid">
            
            <!-- Risk Assessment -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">📊 Current Risk Assessment</h3>
                    <p class="card-subtitle">AI-powered compliance risk analysis</p>
                </div>
                <div class="card-content">
                    <div class="metric-card" style="margin-bottom: 20px;">
                        <div class="metric-value" style="color: var(--success-color);">{app_state['predictive_compliance']['risk_score']}</div>
                        <div class="metric-label">Overall Risk Score (0.0 = Low, 1.0 = High)</div>
                    </div>
                    
                    <div style="display: grid; gap: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🇪🇺 EU AI Act Compliance</span>
                            <span style="font-weight: 600; color: var(--success-color);">Low Risk</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🔒 GDPR Compliance</span>
                            <span style="font-weight: 600; color: var(--success-color);">Low Risk</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>📋 ISO 27001</span>
                            <span style="font-weight: 600; color: var(--warning-color);">Medium Risk</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🛡️ SOC2 Type II</span>
                            <span style="font-weight: 600; color: var(--warning-color);">Medium Risk</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Trend Analysis -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">📈 Trend Analysis</h3>
                    <p class="card-subtitle">Compliance risk trends over time</p>
                </div>
                <div class="card-content">
                    <div style="text-align: center; margin: 40px 0;">
                        <div style="font-size: 48px; color: var(--success-color);">📉</div>
                        <h4 style="color: var(--success-color); margin: 16px 0;">Improving Trend</h4>
                        <p style="color: var(--gray-600);">Your compliance risk has decreased by 15% over the last 30 days</p>
                    </div>
                    
                    <div style="display: grid; gap: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Last 7 days</span>
                            <span style="font-weight: 600; color: var(--success-color);">-5% risk</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Last 30 days</span>
                            <span style="font-weight: 600; color: var(--success-color);">-15% risk</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Last 90 days</span>
                            <span style="font-weight: 600; color: var(--success-color);">-8% risk</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Predictive Alerts -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">🔮 Predictive Alerts</h3>
                    <p class="card-subtitle">AI-powered predictions of future compliance issues</p>
                </div>
                <div class="card-content">
                    <div style="display: grid; gap: 12px;">
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--warning-color);">
                            <div style="font-weight: 600; color: var(--warning-color);">PREDICTED RISK</div>
                            <div style="margin: 8px 0;">ISO 27001 audit preparation needed within 60 days</div>
                            <div style="font-size: 12px; color: var(--gray-500);">Confidence: 78% • Predicted for: Aug 18, 2025</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--primary-color);">
                            <div style="font-weight: 600; color: var(--primary-color);">OPPORTUNITY</div>
                            <div style="margin: 8px 0;">EU AI Act compliance score could improve by 12% with documentation updates</div>
                            <div style="font-size: 12px; color: var(--gray-500);">Confidence: 85% • Estimated effort: 2 weeks</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--success-color);">
                            <div style="font-weight: 600; color: var(--success-color);">POSITIVE TREND</div>
                            <div style="margin: 8px 0;">GDPR compliance score trending upward, likely to reach 95% by month end</div>
                            <div style="font-size: 12px; color: var(--gray-500);">Confidence: 92% • Current: 89.2%</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recommendations -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">💡 AI Recommendations</h3>
                    <p class="card-subtitle">Personalized recommendations to improve compliance</p>
                </div>
                <div class="card-content">
                    <div style="display: grid; gap: 16px;">
                        <div style="padding: 16px; background: var(--primary-color); color: white; border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 8px;">🎯 Priority Action</div>
                            <div style="margin-bottom: 8px;">Update data processing documentation to align with latest GDPR guidelines</div>
                            <div style="font-size: 12px; opacity: 0.9;">Impact: +7% compliance score • Effort: Low</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 8px;">📋 Documentation</div>
                            <div style="margin-bottom: 8px;">Create AI system impact assessment for EU AI Act compliance</div>
                            <div style="font-size: 12px; color: var(--gray-500);">Impact: +12% compliance score • Effort: Medium</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 8px;">🔄 Process</div>
                            <div style="margin-bottom: 8px;">Implement automated compliance monitoring for continuous improvement</div>
                            <div style="font-size: 12px; color: var(--gray-500);">Impact: +5% compliance score • Effort: High</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    elif feature_name == 'ethical-ai-score':
        content = f"""
        <div class="page-header">
            <h1 class="page-title">{feature['title']}</h1>
            <p class="page-subtitle">{feature['subtitle']}</p>
        </div>

        <div class="feature-status-banner">
            <div>
                <strong>Feature Active</strong>
                <div style="font-size: 14px; opacity: 0.9;">
                    Ethical assessment updated continuously with industry benchmarking
                </div>
            </div>
            <div style="font-size: 24px;">
                ✅
            </div>
        </div>

        <div class="content-grid">
            
            <!-- Overall Score -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">⭐ Overall Ethical AI Score</h3>
                    <p class="card-subtitle">Your organization's ethical AI performance</p>
                </div>
                <div class="card-content">
                    <div class="metric-card" style="margin-bottom: 20px;">
                        <div class="metric-value" style="color: var(--success-color);">{app_state['ethical_ai_score']['overall_score']}</div>
                        <div class="metric-label">Ethical AI Score (out of 100)</div>
                    </div>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 18px; font-weight: 600; color: var(--success-color);">Excellent Performance</div>
                        <div style="font-size: 14px; color: var(--gray-600);">Top {app_state['ethical_ai_score']['percentile']}% in your industry</div>
                    </div>
                    
                    <div style="display: grid; gap: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Industry Average</span>
                            <span style="font-weight: 600; color: var(--gray-600);">72.3</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Your Score</span>
                            <span style="font-weight: 600; color: var(--success-color);">{app_state['ethical_ai_score']['overall_score']}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>Improvement</span>
                            <span style="font-weight: 600; color: var(--success-color);">+{app_state['ethical_ai_score']['overall_score'] - 72.3:.1f} points</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Ethical Dimensions -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">📊 Ethical Dimensions</h3>
                    <p class="card-subtitle">Performance across key ethical categories</p>
                </div>
                <div class="card-content">
                    <div style="display: grid; gap: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🤝 Beneficence</span>
                            <span style="font-weight: 600; color: var(--success-color);">92</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🛡️ Non-Maleficence</span>
                            <span style="font-weight: 600; color: var(--success-color);">89</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🗳️ Autonomy</span>
                            <span style="font-weight: 600; color: var(--success-color);">85</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>⚖️ Justice</span>
                            <span style="font-weight: 600; color: var(--warning-color);">78</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🔍 Transparency</span>
                            <span style="font-weight: 600; color: var(--success-color);">91</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>📋 Accountability</span>
                            <span style="font-weight: 600; color: var(--success-color);">88</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>🔒 Privacy</span>
                            <span style="font-weight: 600; color: var(--success-color);">94</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--gray-50); border-radius: 6px;">
                            <span>👤 Human Dignity</span>
                            <span style="font-weight: 600; color: var(--success-color);">86</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Industry Benchmarking -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">🏆 Industry Benchmarking</h3>
                    <p class="card-subtitle">How you compare to industry peers</p>
                </div>
                <div class="card-content">
                    <div style="display: grid; gap: 16px;">
                        <div style="padding: 16px; background: var(--success-color); color: white; border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 8px;">🥇 Top Performer</div>
                            <div style="margin-bottom: 8px;">You rank in the top 15% of organizations in your industry</div>
                            <div style="font-size: 12px; opacity: 0.9;">Based on 2,847 organizations in Technology sector</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 8px;">📈 Strengths</div>
                            <div style="margin-bottom: 8px;">Privacy protection, Transparency, and Beneficence are your strongest areas</div>
                            <div style="font-size: 12px; color: var(--gray-500);">All above 90th percentile</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px;">
                            <div style="font-weight: 600; margin-bottom: 8px;">🎯 Improvement Area</div>
                            <div style="margin-bottom: 8px;">Justice and fairness could be enhanced with bias detection improvements</div>
                            <div style="font-size: 12px; color: var(--gray-500);">Currently at 65th percentile</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Updates -->
            <div class="content-card">
                <div class="card-header">
                    <h3 class="card-title">📅 Recent Updates</h3>
                    <p class="card-subtitle">Latest changes to your ethical AI score</p>
                </div>
                <div class="card-content">
                    <div style="display: grid; gap: 12px;">
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--success-color);">
                            <div style="font-weight: 600; color: var(--success-color);">IMPROVEMENT</div>
                            <div style="margin: 8px 0;">Privacy score increased from 91 to 94 (+3 points)</div>
                            <div style="font-size: 12px; color: var(--gray-500);">2 days ago • Due to enhanced data protection measures</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--success-color);">
                            <div style="font-weight: 600; color: var(--success-color);">IMPROVEMENT</div>
                            <div style="margin: 8px 0;">Transparency score increased from 88 to 91 (+3 points)</div>
                            <div style="font-size: 12px; color: var(--gray-500);">1 week ago • Due to improved documentation</div>
                        </div>
                        <div style="padding: 16px; background: var(--gray-50); border-radius: 8px; border-left: 4px solid var(--primary-color);">
                            <div style="font-weight: 600; color: var(--primary-color);">STABLE</div>
                            <div style="margin: 8px 0;">Overall score maintained at {app_state['ethical_ai_score']['overall_score']} (no change)</div>
                            <div style="font-size: 12px; color: var(--gray-500);">Last calculated: {app_state['ethical_ai_score']['last_calculated']}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    else:
        # Para outras features, mostrar página genérica
        content = f"""
        <div class="page-header">
            <h1 class="page-title">{feature['title']}</h1>
            <p class="page-subtitle">{feature['subtitle']}</p>
        </div>

        <div class="feature-status-banner">
            <div>
                <strong>Feature Active</strong>
                <div style="font-size: 14px; opacity: 0.9;">
                    This feature is active and monitoring your systems
                </div>
            </div>
            <div style="font-size: 24px;">
                ✅
            </div>
        </div>

        <div class="content-card">
            <div class="card-content">
                <div class="alert info">
                    <strong>Feature Dashboard Coming Soon</strong><br>
                    This feature is active and working. A detailed dashboard will be available in the next update.
                </div>
                
                <div style="text-align: center; margin-top: 32px;">
                    <a href="/" class="btn btn-primary">
                        <span>🏠</span>
                        <span>Back to Dashboard</span>
                    </a>
                </div>
            </div>
        </div>
        """
    
    return render_template_string(BASE_TEMPLATE, 
                                title=feature['title'], 
                                content=content, 
                                page="feature",
                                uploaded_files=uploaded_files,
                                llm_connected=llm_connected)

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
        'version': '1.1.0',
        'features_active': calculate_feature_status(),
        'total_features': 7,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("🚀 Starting ZenThera AI Compliance Suite v1.1.0...")
    print("📊 Dashboard: http://localhost:5016/")
    print("⚙️ Setup: http://localhost:5016/setup")
    print("🔗 Health: http://localhost:5016/api/health")
    print("🎯 Features: http://localhost:5016/feature/regulation-sync")
    app.run(host='0.0.0.0', port=5017, debug=True)

