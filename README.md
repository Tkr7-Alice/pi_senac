PIBot v2 🤖
Projeto Integrador SENAC desenvolvido com Flask, Python, SQLite e integração com IA Gemini.

🚀 Tecnologias
Python
Frasco
SQLite
HTML
CSS
JavaScript
API Gemini
📁 Estrutura
pi_senac/
│
├── back/
├── assets/
├── scripts/
├── styles/
├── index.html
├── admin.html
└── README.md
⚙️ Como executar
1. Clonar o projeto
git clone SEU_LINK_GITHUB
2. Entre na pasta
cd pi_senac
3. Instale as responsabilidades
pip install -r requirements.txt
4. Configure o arquivo.env
Dentro da massa back/:

IA_PROVIDER=gemini

GEMINI_API_KEY=SUA_CHAVE

GEMINI_MODEL=gemini-2.0-flash

IA_URL=https://generativelanguage.googleapis.com/v1beta/models
5. Execute o projeto
python app.py
🌐 Rotas principais
Página	URL
Chatbot	/
Painel	/admin.html
Conversas JSON	/api/conversas
Registros	/admin/api/logs
Estatísticas	/admin/api/stats
🔒 Segurança
O sistema possui:

Validação de entrada
base contra XSS
Registro de incidentes
Monitoramento de atividades
👨‍💻 Projeto SENAC
Projeto desenvolvido para fins acadêmicos no SENAC.

Lançamentos
Nenhuma versão publicada
Criar uma nova versão
Pacotes
Nenhum pacote publicado.
Publique seu primeiro pacote.
Colaboradores
1
@Tkr7-Alice
Tkr7-Alice Thomas
Línguas
CSS
34,4%
 
HTML
25,3%
 
Python
22,3%
 
JavaScript
18,0%
Fluxos de trabalho sugeridos
Com base na sua pilha de tecnologias.
Logotipo do Webpack
Webpack
Crie um projeto NodeJS com npm e webpack.
Logotipo Deno
Deno
Teste seu projeto Deno
Pacote Python usando o logotipo do Anaconda
Pacote Python usando Anaconda
Crie e teste um pacote Python em várias versões do Python usando o Anaconda para gerenciamento de pacotes
