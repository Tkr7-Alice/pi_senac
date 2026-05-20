import os
import requests


class IAService:

    SYSTEM_PROMPT = (
        "Você é o PIBot, um assistente inteligente "
        "do Projeto Integrador do SENAC.\n"

        "Sua personalidade é tecnológica, amigável, "
        "didática e futurista.\n"

        "Responda de forma clara, natural e útil.\n"

        "Explique assuntos difíceis de forma simples.\n"

        "Você pode responder perguntas sobre "
        "tecnologia, programação, front-end, backend, "
        "Python, inteligência artificial e temas gerais.\n"

        "Evite respostas muito longas, mas seja completo "
        "quando necessário."
    )

    @classmethod
    def perguntar_ia(cls, mensagem):

        # =========================
        # Validação básica
        # =========================

        if not mensagem:

            return {
                "success": False,
                "response": "Mensagem vazia."
            }

        mensagem = str(mensagem).strip()

        if len(mensagem) > 2000:

            return {
                "success": False,
                "response": "Mensagem muito longa."
            }

        provider = os.getenv(
            "IA_PROVIDER",
            "gemini"
        ).lower()

        try:

            # =========================
            # GEMINI
            # =========================

            if provider == "gemini":

                api_key = os.getenv(
                    "GEMINI_API_KEY"
                )

                model = os.getenv(
                    "GEMINI_MODEL",
                    "gemini-1.5-flash"
                )

                base_url = os.getenv(
                    "IA_URL"
                )

                if not api_key:

                    print(
                        "[IA] GEMINI_API_KEY não encontrada."
                    )

                    return {
                        "success": False,
                        "response": "API Gemini não configurada."
                    }

                url = (
                    f"{base_url}/"
                    f"{model}:generateContent"
                )

                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": (
                                        cls.SYSTEM_PROMPT +
                                        "\n\nUsuário: " +
                                        mensagem
                                    )
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 40
                    }
                }

                response = requests.post(
                    url,
                    params={
                        "key": api_key
                    },
                    headers={
                        "Content-Type":
                        "application/json"
                    },
                    json=payload,
                    timeout=15
                )

                # =========================
                # LIMITE DA API
                # =========================

                if response.status_code == 429:

                    print(
                        "[IA] Limite da API atingido."
                    )

                    return {
                        "success": False,
                        "response": (
                            "A IA está temporariamente ocupada. "
                            "Tente novamente em alguns segundos."
                        )
                    }

                # =========================
                # OUTROS ERROS
                # =========================

                if response.status_code != 200:

                    print(
                        f"[IA ERROR] {response.status_code}"
                    )

                    print(response.text)

                    return {
                        "success": False,
                        "response": (
                            "Erro ao consultar Gemini."
                        )
                    }

                data = response.json()

                return {
                    "success": True,
                    "response": (
                        data["candidates"][0]
                        ["content"]["parts"][0]
                        ["text"]
                    )
                }

            # =========================
            # OPENAI
            # =========================

            elif provider == "openai":

                api_key = os.getenv(
                    "OPENAI_API_KEY"
                )

                if not api_key:

                    return {
                        "success": False,
                        "response": "API OpenAI não configurada."
                    }

                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization":
                        f"Bearer {api_key}",
                        "Content-Type":
                        "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system",
                                "content":
                                cls.SYSTEM_PROMPT
                            },
                            {
                                "role": "user",
                                "content": mensagem
                            }
                        ],
                        "temperature": 0.5,
                        "max_tokens": 150
                    },
                    timeout=15
                )

                if response.status_code != 200:

                    print(
                        f"[OPENAI ERROR] {response.status_code}"
                    )

                    print(response.text)

                    return {
                        "success": False,
                        "response": "Erro ao consultar OpenAI."
                    }

                data = response.json()

                return {
                    "success": True,
                    "response": (
                        data["choices"][0]
                        ["message"]["content"]
                    )
                }

            # =========================
            # PROVIDER INVÁLIDO
            # =========================

            else:

                return {
                    "success": False,
                    "response": "Provider inválido."
                }

        except Exception as erro:

            print(
                f"[IA EXCEPTION] {erro}"
            )

            return {
                "success": False,
                "response": "Erro interno da IA."
            }