# PIBot v2 🤖

Projeto Integrador SENAC desenvolvido com Flask, Python, SQLite e integração com IA Gemini.

## 🚀 Tecnologias

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Gemini API

---

## 📁 Estrutura

```bash
pi_senac/
│
├── back/
├── assets/
├── scripts/
├── styles/
├── index.html
├── admin.html
└── README.md
```

---

## ⚙️ Como executar

### 1. Clone o projeto

```bash
git clone SEU_LINK_GITHUB
```

---

### 2. Entre na pasta

```bash
cd pi_senac
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configure o arquivo `.env`

Dentro da pasta `back/`:

```env
IA_PROVIDER=gemini

GEMINI_API_KEY=SUA_CHAVE

GEMINI_MODEL=gemini-2.0-flash

IA_URL=https://generativelanguage.googleapis.com/v1beta/models
```

---

### 5. Execute o projeto

```bash
python app.py
```

---

## 🌐 Rotas principais

| Página | URL |
|---|---|
| Chatbot | `/` |
| Dashboard | `/admin.html` |
| Conversas JSON | `/api/conversas` |
| Logs | `/admin/api/logs` |
| Estatísticas | `/admin/api/stats` |

---

## 🔒 Segurança

O sistema possui:

- Validação de entrada
- Proteção básica contra XSS
- Registro de incidentes
- Monitoramento de atividades

---

## 👨‍💻 Projeto SENAC

Projeto desenvolvido para fins acadêmicos no SENAC.