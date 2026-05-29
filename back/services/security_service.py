import re
from services.db_service import DBService

class SecurityService:
    _lockdown_active = False
    _malicious_patterns = [
        re.compile(r"script", re.IGNORECASE),
        re.compile(r"onerror\s*=", re.IGNORECASE),
        re.compile(r"javascript:", re.IGNORECASE),
        re.compile(r"iframe", re.IGNORECASE)
    ]

    @classmethod
    def is_lockdown_active(cls):
        return cls._lockdown_active

    @classmethod
    def activate_lockdown(cls):
        cls._lockdown_active = True

    @classmethod
    def deactivate_lockdown(cls):
        cls._lockdown_active = False

    @classmethod
    def check_input_safety(cls, text, ip_address=None):
        if not text:
            return {"safe": True, "resposta": None, "trigger_security_scene": False, "action": None}

        normalized = text.strip().lower()

        if normalized == "desativar lockdown":
            if cls._lockdown_active:
                cls.deactivate_lockdown()
                DBService.registrar_incidente(text, ip_address, "lockdown_reset")
                return {
                    "safe": True,
                    "resposta": "Protocolo de segurança desativado. Sistemas reiniciados.",
                    "trigger_security_scene": False,
                    "action": "reset"
                }
            return {
                "safe": True,
                "resposta": "O sistema já está operando normalmente.",
                "trigger_security_scene": False,
                "action": None
            }

        if cls._lockdown_active:
            return {
                "safe": False,
                "resposta": "Acesso negado. Sistema em lockdown.",
                "trigger_security_scene": False,
                "action": None
            }

        for pattern in cls._malicious_patterns:
            if pattern.search(normalized):
                cls.activate_lockdown()
                DBService.registrar_incidente(text, ip_address, "lockdown_active")
                return {
                    "safe": False,
                    "resposta": "ATENÇÃO. Tentativa de intrusão detectada. Protocolo de segurança ativado.",
                    "trigger_security_scene": True,
                    "action": None
                }

        return {"safe": True, "resposta": None, "trigger_security_scene": False, "action": None}