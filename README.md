# 🤖 PIBot v2

> Assistente virtual inteligente desenvolvido para o **Projeto Integrador SENAC** utilizando **Flask, Python, SQLite** e integração com **Google Gemini AI**.

---

## 🚀 Tecnologias Utilizadas

* **Python**
* **Flask**
* **SQLite**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Google Gemini API**

---

## 📁 Estrutura do Projeto

```text
pi_senac/
│
├── back/
│   ├── routes/
│   ├── services/
│   └── app.py
│
├── assets/
│   └── images/
│
├── scripts/
├── styles/
│
├── index.html
├── admin.html
├── requirements.txt
└── README.md
```

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/Tkr7-Alice/pi_senac.git
```

### 2️⃣ Entrar na pasta do projeto

```bash
cd pi_senac
```

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar o arquivo `.env`

Crie o arquivo `.env` dentro da pasta `back/`.

```env
IA_PROVIDER=gemini

GEMINI_API_KEY=SUA_CHAVE

GEMINI_MODEL=gemini-2.0-flash

IA_URL=https://generativelanguage.googleapis.com/v1beta/models
```

### 5️⃣ Executar a aplicação

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://localhost:5000
```

---

## 🌐 Rotas Principais

| Funcionalidade        | Endpoint                |
| --------------------- | ----------------------- |
| Chat Principal        | `/`                     |
| Painel Administrativo | `/admin`                |
| Conversas JSON        | `/api/conversas`        |
| Estatísticas          | `/admin/api/stats`      |
| Logs                  | `/admin/api/logs`       |
| Incidentes            | `/admin/api/incidentes` |

---

## 🔒 Recursos de Segurança

O sistema possui:

* ✅ Validação de entrada
* ✅ Proteção básica contra XSS
* ✅ Registro de incidentes
* ✅ Sistema de Lockdown
* ✅ Monitoramento de atividades suspeitas
* ✅ Histórico de conversas

---

## 📊 Funcionalidades

* Chat inteligente com IA Gemini
* Respostas locais para perguntas frequentes
* Dashboard administrativo
* Estatísticas em tempo real
* Registro de conversas
* Registro de incidentes de segurança
* Modo de contingência (fallback offline)

---

## 👨‍💻 Desenvolvedor

**Thomas Kirmeier**

Projeto desenvolvido para fins acadêmicos no **SENAC**.

---

## 📄 Licença

Este projeto foi desenvolvido exclusivamente para fins educacionais e acadêmicos.
