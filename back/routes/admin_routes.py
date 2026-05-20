from flask import Blueprint, jsonify, current_app
from services.db_service import DBService
from services.security_service import SecurityService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_page():
    """Serve a página HTML do Dashboard Admin."""
    return current_app.send_static_file('admin.html')

@admin_bp.route('/admin/api/stats')
def get_stats():
    """Endpoint que retorna estatísticas e status atual do robô."""
    stats = DBService.obter_estatisticas()
    stats["lockdown_active"] = SecurityService.is_lockdown_active()
    return jsonify(stats)

@admin_bp.route('/admin/api/logs')
def get_logs():
    """Endpoint que retorna o histórico das últimas conversas."""
    logs = DBService.obter_logs(limite=50)
    return jsonify(logs)

@admin_bp.route('/admin/api/incidentes')
def get_incidents():
    """Endpoint que retorna os logs de incidentes de segurança."""
    incidents = DBService.obter_incidentes(limite=50)
    return jsonify(incidents)
