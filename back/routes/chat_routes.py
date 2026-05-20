from flask import Blueprint, request, jsonify
from services.security_service import SecurityService
from services.ia_service import IAService
from services.db_service import DBService

chat_bp = Blueprint('chat', __name__)

# Intenções locais portadas para o backend
INTENTS = [
    {
        "keywords": ["python"],
        "response": "Python é uma linguagem simples e poderosa usada em automação, IA e backend.",
        "mediaType": "image",
        "mediaSrc": "assets/images/python.png"
    },
    {
        "keywords": ["backend", "back-end", "back end"],
        "response": "Backend funciona como o cérebro do sistema.",
        "mediaType": "image",
        "mediaSrc": "assets/images/backend.png"
    },
    {
        "keywords": ["ia", "inteligência artificial", "inteligencia artificial", "ai"],
        "response": "Inteligência Artificial permite que sistemas aprendam com dados e tomem decisões automatizadas para resolver problemas complexos.",
        "mediaType": "image",
        "mediaSrc": "assets/images/ia.png"
    },
    {
        "keywords": ["senac", "projeto", "pi"],
        "response": "O Projeto Integrador do SENAC é a oportunidade de unir teoria e prática, criando soluções reais e tecnológicas.",
        "mediaType": "none",
        "mediaSrc": ""
    },
    {
        "keywords": ["oi", "olá", "ola", "bom dia", "boa noite"],
        "response": "Olá. Bem-vindos à nossa apresentação. Como posso demonstrar minhas funções hoje?",
        "mediaType": "none",
        "mediaSrc": ""
    }
]

@chat_bp.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.get_json() or {}
    mensagem = data.get("mensagem", "").strip()
    ip_address = request.remote_addr

    # 1. Validação de Segurança e Lockdown
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

    # 2. Verificar Intenções Locais
    import re
    lower_msg = mensagem.lower()
    found_intent = None
    for intent in INTENTS:
        match = False
        for keyword in intent["keywords"]:
            if len(keyword) <= 3:
                # Usa regex com \b para bater palavra inteira
                if re.search(r'\b' + re.escape(keyword) + r'\b', lower_msg):
                    match = True
                    break
            else:
                if keyword in lower_msg:
                    match = True
                    break
        if match:
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

    # 3. Consultar IA Externa
    ia_resposta = IAService.perguntar_ia(
        mensagem
    )
    if ia_resposta and ia_resposta.get("success"):
        resposta_txt = (
            ia_resposta["response"]
        )
        DBService.registrar_conversa(mensagem, resposta_txt, "ia")
        return jsonify({
            "resposta": resposta_txt,
            "mediaType": "none",
            "mediaSrc": "",
            "lockdown": False,
            "trigger_security_scene": False,
            "action": None
        })

    # 4. Caso a IA falhe (Modo Offline / Sem chave)
    resposta_fallback = (
        ia_resposta["response"]
    )
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