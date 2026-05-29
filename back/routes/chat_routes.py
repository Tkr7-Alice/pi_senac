import re
from flask import Blueprint, request, jsonify
from services.security_service import SecurityService
from services.ia_service import IAService
from services.db_service import DBService

chat_bp = Blueprint('chat', __name__)

INTENTS = [
    {"keywords": [re.compile(r'\bpython\b')], "response": "Python é uma linguagem simples e poderosa usada em automação, IA e backend.", "mediaType": "image", "mediaSrc": "assets/images/python.png"},
    {"keywords": [re.compile(r'\bback[- ]?end\b')], "response": "Backend funciona como o cérebro do sistema.", "mediaType": "image", "mediaSrc": "assets/images/backend.png"},
    {"keywords": [re.compile(r'\bia\b'), re.compile(r'\bai\b'), re.compile(r'inteligên?cia artificial')], "response": "Inteligência Artificial permite que sistemas aprendam com dados e tomem decisões.", "mediaType": "image", "mediaSrc": "assets/images/ia.png"},
    {"keywords": [re.compile(r'\bsenac\b'), re.compile(r'\bpi\b')], "response": "O Projeto Integrador do SENAC une teoria e prática, criando soluções reais.", "mediaType": "none", "mediaSrc": ""},
    {"keywords": [re.compile(r'\boi\b'), re.compile(r'\bolá\b'), re.compile(r'\bboa[ -](dia|noite|tarde)\b')], "response": "Olá. Bem-vindos à nossa apresentação. Como posso demonstrar minhas funções hoje?", "mediaType": "none", "mediaSrc": ""}
]

@chat_bp.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.get_json() or {}
    mensagem = data.get("mensagem", "").strip()
    ip_address = request.remote_addr

    security_check = SecurityService.check_input_safety(mensagem, ip_address=ip_address)
    if not security_check["safe"] or security_check["action"] == "reset":
        return jsonify({
            "resposta": security_check["resposta"],
            "mediaType": "none",
            "mediaSrc": "",
            "lockdown": SecurityService.is_lockdown_active(),
            "trigger_security_scene": security_check["trigger_security_scene"],
            "action": security_check["action"]
        })

    normalized = mensagem.lower()
    found_intent = None
    
    for intent in INTENTS:
        if any(pattern.search(normalized) for pattern in intent["keywords"]):
            found_intent = intent
            break

    if found_intent:
        resposta_txt = found_intent["response"]
        DBService.registrar_conversa(mensagem, resposta_txt, "local")
        return jsonify({
            "resposta": resposta_txt,
            "mediaType": found_intent["mediaType"],
            "mediaSrc": found_intent["mediaSrc"],
            "lockdown": False,
            "trigger_security_scene": False,
            "action": None
        })

    ia_resposta = IAService.perguntar_ia(mensagem)
    if ia_resposta and ia_resposta.get("success"):
        resposta_txt = ia_resposta["response"]
        DBService.registrar_conversa(mensagem, resposta_txt, "ia")
        return jsonify({
            "resposta": resposta_txt,
            "mediaType": "none",
            "mediaSrc": "",
            "lockdown": False,
            "trigger_security_scene": False,
            "action": None
        })

    resposta_fallback = ia_resposta.get("response", "Modo offline ativo. Falha na comunicação com os servidores centrais.")
    DBService.registrar_conversa(mensagem, resposta_fallback, "offline_fallback")
    return jsonify({
        "resposta": resposta_fallback,
        "mediaType": "none",
        "mediaSrc": "",
        "lockdown": False,
        "trigger_security_scene": False,
        "action": "offline_fallback"
    })

@chat_bp.route('/api/conversas', methods=['GET'])
def listar_conversas():
    conversas = DBService.listar_conversas()
    return jsonify({
        "success": True,
        "total": len(conversas),
        "data": conversas
    })