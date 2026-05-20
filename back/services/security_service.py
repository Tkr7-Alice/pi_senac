import re

class SecurityService:
    _lockdown_active = False

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
        """
        Verifica se a entrada é segura.
        Retorna um dicionário com os campos:
        - safe: bool
        - resposta: str ou None
        - trigger_security_scene: bool
        - action: str ou None
        """
        if not text:
            return {"safe": True, "resposta": None, "trigger_security_scene": False, "action": None}

        # Normaliza a entrada
        normalized = text.strip().lower()

        # Importa dinamicamente para evitar imports circulares
        from services.db_service import DBService

        # Comando especial para desativar o lockdown
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
            else:
                return {
                    "safe": True,
                    "resposta": "O sistema já está operando normalmente. Protocolo de segurança inativo.",
                    "trigger_security_scene": False,
                    "action": None
                }

        # Se o sistema já estiver em lockdown
        if cls._lockdown_active:
            return {
                "safe": False,
                "resposta": "Acesso negado. Sistema em lockdown.",
                "trigger_security_scene": False,
                "action": None
            }

        # Detecção de assinaturas maliciosas (Script Injection)
        malicious_patterns = [
            r"script",
            r"onerror\s*=",
            r"javascript:",
            r"iframe"
        ]

        for pattern in malicious_patterns:
            if re.search(pattern, normalized):
                cls.activate_lockdown()
                DBService.registrar_incidente(text, ip_address, "lockdown_active")
                return {
                    "safe": False,
                    "resposta": "ATENÇÃO. Tentativa de intrusão detectada. Protocolo de segurança ativado.",
                    "trigger_security_scene": True,
                    "action": None
                }

        return {"safe": True, "resposta": None, "trigger_security_scene": False, "action": None}
