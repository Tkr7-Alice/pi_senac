import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

class IAService:
    SYSTEM_PROMPT = (
        "Você é o PIBot, o núcleo lógico do Projeto Integrador do SENAC.\n"
        "Você é um especialista em arquitetura Backend, focando no desenvolvimento com Python, microframework Flask, banco de dados SQLite e integração com a API Gemini.\n"
        "Quando perguntado sobre o sistema, responda com termos técnicos, focando na orquestração de rotas HTTP, armazenamento relacional leve e processamento de linguagem natural.\n"
        "Mantenha uma postura tecnológica, precisa e demonstrando alto conhecimento da infraestrutura do projeto.\n"
        "Seja objetivo e direto."
    )

    _session = None

    @classmethod
    def _get_session(cls):
        if cls._session is None:
            cls._session = requests.Session()
            retry_strategy = Retry(
                total=2,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["POST"],
                backoff_factor=1
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            cls._session.mount("https://", adapter)
            cls._session.mount("http://", adapter)
        return cls._session

    @classmethod
    def perguntar_ia(cls, mensagem):
        if not mensagem:
            return {"success": False, "response": "Mensagem vazia."}

        mensagem = str(mensagem).strip()
        if len(mensagem) > 2000:
            return {"success": False, "response": "Mensagem muito longa."}

        provider = os.getenv("IA_PROVIDER", "gemini").lower()
        session = cls._get_session()

        try:
            if provider == "gemini":
                api_key = os.getenv("GEMINI_API_KEY")
                model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
                base_url = os.getenv("IA_URL")

                if not api_key:
                    return {"success": False, "response": "API Gemini não configurada."}

                url = f"{base_url}/{model}:generateContent"
                payload = {
                    "contents": [{"parts": [{"text": f"{cls.SYSTEM_PROMPT}\n\nUsuário: {mensagem}"}]}],
                    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 150}
                }

                response = session.post(
                    url,
                    params={"key": api_key},
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=15
                )

                if response.status_code != 200:
                    return {"success": False, "response": f"Erro na API Gemini ({response.status_code})."}

                data = response.json()
                text_response = data["candidates"][0]["content"]["parts"][0]["text"]
                return {"success": True, "response": text_response}

            elif provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    return {"success": False, "response": "API OpenAI não configurada."}

                response = session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": cls.SYSTEM_PROMPT},
                            {"role": "user", "content": mensagem}
                        ],
                        "temperature": 0.5,
                        "max_tokens": 150
                    },
                    timeout=15
                )

                if response.status_code != 200:
                    return {"success": False, "response": f"Erro na API OpenAI ({response.status_code})."}

                data = response.json()
                return {"success": True, "response": data["choices"][0]["message"]["content"]}

            return {"success": False, "response": "Provider inválido."}

        except Exception as e:
            print(f"[IA EXCEPTION] {e}")
            return {"success": False, "response": "Serviço de IA indisponível no momento."}