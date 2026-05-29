from flask import Blueprint, jsonify, current_app
from services.db_service import DBService
from services.security_service import SecurityService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_page():
    return current_app.send_static_file('admin.html')

@admin_bp.route('/admin/api/stats')
def get_stats():
    stats = DBService.obter_estatisticas()
    stats["lockdown_active"] = SecurityService.is_lockdown_active()
    return jsonify(stats)

@admin_bp.route('/admin/api/logs')
def get_logs():
    return jsonify(DBService.obter_logs(limite=50))

@admin_bp.route('/admin/api/incidentes')
def get_incidents():
    return jsonify(DBService.obter_incidentes(limite=50))