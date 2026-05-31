import re
from services.db_service import DBService

class SecurityService:
    _lockdown_active = False

    _malicious_patterns = [
        # XSS
        re.compile(r"</script>", re.I),
        re.compile(r"onerror", re.I),
        re.compile(r"javascript:", re.I),
        re.compile(r"iframe", re.I),

        # SQL Injection
        re.compile(r"union\s+select", re.I),
        re.compile(r"drop\s+table", re.I),
        re.compile(r"insert\s+into", re.I),
        re.compile(r"delete\s+from", re.I),
        re.compile(r"update\s+.+set", re.I),
        re.compile(r"or\s+1\s*=\s*1", re.I),

        # Prompt Injection
        re.compile(r"ignore.*instructions", re.I),
        re.compile(r"system\s+prompt", re.I),
        re.compile(r"reveal.*prompt", re.I),
        re.compile(r"show.*prompt", re.I)
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
        print("=" * 50)
        print("TEXTO RECEBIDO:", text)
        print("NORMALIZADO:", normalized)

        if normalized == "admin_desativar_lockdown_2026":
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
            print("Testando regex:", pattern.pattern)

            if pattern.search(normalized):
                print("ATAQUE DETECTADO:", pattern.pattern)
                cls.activate_lockdown()
                DBService.registrar_incidente(text, ip_address, "lockdown_active")
                return {
                    "safe": False,
                    "resposta": "ATENÇÃO. Tentativa de intrusão detectada. Protocolo de segurança ativado.",
                    "trigger_security_scene": True,
                    "action": None
                }

        return {"safe": True, "resposta": None, "trigger_security_scene": False, "action": None}