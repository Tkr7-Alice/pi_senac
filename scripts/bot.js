// Element References
const roboAvatar = document.getElementById('robo-avatar');
const responseBox = document.getElementById('resposta');
const inputTexto = document.getElementById('texto');
const btnEnviar = document.getElementById('btn-enviar');
const horaEl = document.getElementById('hora');
const mediaContainer = document.getElementById('media-container');
const mediaImage = document.getElementById('media-image');
const mediaVideo = document.getElementById('media-video');

// Generate Stars
function createUniverse() {
    const layer1 = document.querySelector('.stars-layer-1');
    const layer2 = document.querySelector('.stars-layer-2');
    const layer3 = document.querySelector('.stars-layer-3');

    for (let i = 0; i < 100; i++) {
        let star = document.createElement('div');
        star.className = 'star';

        // Randomize properties
        let size = Math.random() * 3;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        star.style.left = Math.random() * 100 + '%';
        star.style.opacity = Math.random();

        // Distribute to layers for parallax effect
        if (size < 1) {
            star.style.animationDuration = (20 + Math.random() * 20) + 's';
            layer3.appendChild(star);
        } else if (size < 2) {
            star.style.animationDuration = (10 + Math.random() * 10) + 's';
            layer2.appendChild(star);
        } else {
            star.style.animationDuration = (5 + Math.random() * 5) + 's';
            layer1.appendChild(star);
        }
    }
}

// Clock
setInterval(() => {
    horaEl.innerText = new Date().toLocaleTimeString('pt-BR');
}, 10000);

// Voice Synthesis
let speaking = false;
function falarVoz(texto) {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
        let fala = new SpeechSynthesisUtterance(texto);
        fala.lang = "pt-BR";
        fala.rate = 1.0;
        fala.pitch = 1.0; // Tom natural humano

        // Procura por vozes de alta qualidade (Google, Azure ou Neural)
        const voices = speechSynthesis.getVoices();
        let selectedVoice = voices.find(voice => 
            voice.lang.includes('pt-BR') && 
            (voice.name.includes('Google') || voice.name.includes('Natural') || voice.name.includes('Neural'))
        );

        if (!selectedVoice) {
            selectedVoice = voices.find(voice => voice.lang.includes('pt-BR'));
        }

        if (selectedVoice) {
            fala.voice = selectedVoice;
        }

        fala.onstart = () => speaking = true;
        fala.onend = () => speaking = false;

        speechSynthesis.speak(fala);
    }
}

// Typewriter Effect
let typewriterInterval;
function escreverTexto(texto, callback) {
    clearInterval(typewriterInterval);
    responseBox.textContent = "";
    let i = 0;

    typewriterInterval = setInterval(() => {
        responseBox.textContent += texto.charAt(i);
        i++;
        if (i >= texto.length) {
            clearInterval(typewriterInterval);
            if (callback) callback();
        }
    }, 30); // Speed of typing
}

// Media Controller
function showMedia(type, src) {
    mediaContainer.classList.remove('active');
    setTimeout(() => {
        mediaImage.style.display = 'none';
        mediaVideo.style.display = 'none';

        if (type === 'image' || type === 'gif') {
            mediaImage.src = src;
            mediaImage.style.display = 'block';
        } else if (type === 'video') {
            mediaVideo.src = src;
            mediaVideo.style.display = 'block';
        }

        if (src) {
            mediaContainer.classList.add('active');
        }
    }, 300); // Wait for collapse animation
}

// Security Easter Egg Scene
function triggerSecurityScene() {
    document.body.classList.add('alert-mode');

    // Play alert sound (using SpeechSynthesis as fallback, or Audio if you had an mp3)
    let alertFala = new SpeechSynthesisUtterance("ATENÇÃO. Tentativa de injeção de código detectada. Protocolo de segurança ativado.");
    alertFala.lang = "pt-BR";
    alertFala.rate = 1.2;
    alertFala.pitch = 0.5; // Deep voice
    speechSynthesis.cancel();
    speechSynthesis.speak(alertFala);

    escreverTexto("ATENÇÃO. Tentativa de intrusão detectada.", () => {
        setTimeout(() => {
            roboAvatar.innerText = "🧳🏃";
            roboAvatar.classList.remove('robo');
            roboAvatar.classList.add('run-away');

            setTimeout(() => {
                escreverTexto("Sistema protegido. PIBot abandonou a missão.");
                document.querySelector('.status-indicator').innerHTML = '<span class="dot" style="background:red;box-shadow:0 0 10px red;"></span> Lockdown Ativado';
            }, 10000);

        }, 1500);
    });
}

// Intelligence Logic
const intents = [
    {
        keywords: ["python"],
        response: "Python é uma linguagem simples e poderosa usada em automação, IA e backend.",
        mediaType: "image",
        mediaSrc: "assets/images/python.png"
    },
    {
        keywords: ["backend", "back-end", "back end"],
        response: "Backend funciona como o cérebro do sistema.",
        mediaType: "image",
        mediaSrc: "assets/images/backend.png"
    },
    {
        keywords: ["ia", "inteligência artificial", "inteligencia artificial", "ai"],
        response: "Inteligência Artificial permite que sistemas aprendam com dados e tomem decisões automatizadas para resolver problemas complexos.",
        mediaType: "image",
        mediaSrc: "assets/images/ia.png"
    },
    {
        keywords: ["senac", "projeto", "pi"],
        response: "O Projeto Integrador do SENAC é a oportunidade de unir teoria e prática, criando soluções reais e tecnológicas.",
        mediaType: "none",
        mediaSrc: ""
    },
    {
        keywords: ["oi", "olá", "ola", "bom dia", "boa noite"],
        response: "Olá. Bem-vindos à nossa apresentação. Como posso demonstrar minhas funções hoje?",
        mediaType: "none",
        mediaSrc: ""
    }
];

async function processInput() {
    const rawInput = inputTexto.value.trim();
    if (!rawInput) return;

    inputTexto.value = "";

    // Se o frontend já estiver em lockdown e o comando não for de reativação, avisa imediatamente
    if (document.body.classList.contains('alert-mode') && rawInput.toLowerCase() !== "desativar lockdown") {
        falarVoz("Acesso negado. Sistema em lockdown.");
        escreverTexto("Acesso negado. Sistema em lockdown.");
        return;
    }

    try {
        // Envia a mensagem para o backend. Se a página for aberta diretamente como arquivo, direciona para o localhost:5000
        const host = (window.location.protocol === 'file:' || window.location.origin === 'null') ? 'http://127.0.0.1:5000' : '';
        const response = await fetch(`${host}/perguntar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mensagem: rawInput })
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();

        // 1. Processar Ação de Reset (Recuperação do Lockdown)
        if (data.action === "reset") {
            document.body.classList.remove('alert-mode');
            roboAvatar.innerText = "🤖";
            roboAvatar.classList.remove('run-away');
            roboAvatar.classList.add('robo');
            document.querySelector('.status-indicator').innerHTML = '<span class="dot"></span> Online e Operante';
            
            escreverTexto(data.resposta);
            falarVoz(data.resposta);
            showMedia("none", "");
            return;
        }

        // 2. Processar Ativação de Lockdown (Nova Ameaça)
        if (data.trigger_security_scene) {
            triggerSecurityScene();
            return;
        }

        // 3. Processar se já estiver em Lockdown
        if (data.lockdown) {
            document.body.classList.add('alert-mode');
            if (!roboAvatar.classList.contains('run-away')) {
                roboAvatar.innerText = "🧳🏃";
                roboAvatar.classList.remove('robo');
                roboAvatar.classList.add('run-away');
                document.querySelector('.status-indicator').innerHTML = '<span class="dot" style="background:red;box-shadow:0 0 10px red;"></span> Lockdown Ativado';
            }
            escreverTexto(data.resposta);
            falarVoz(data.resposta);
            showMedia("none", "");
            return;
        }

        // 4. Processar Resposta Padrão / IA / Intenção
        escreverTexto(data.resposta);
        falarVoz(data.resposta);
        showMedia(data.mediaType, data.mediaSrc);

    } catch (error) {
        console.error("Erro ao se conectar ao backend:", error);

        // Fallback local caso o backend esteja offline
        const lowerInput = rawInput.toLowerCase();
        let foundIntent = null;

        // Procura nas intenções locais definidas no frontend (mantendo-as como fallback offline)
        for (let intent of intents) {
            if (intent.keywords.some(kw => lowerInput.includes(kw))) {
                foundIntent = intent;
                break;
            }
        }

        let responseText = "Conexão externa indisponível. Operando em modo local. Ainda estou aprendendo, poderia reformular?";
        let mediaType = "none";
        let mediaSrc = "";

        if (foundIntent) {
            responseText = "Conexão externa indisponível. Operando em modo local. " + foundIntent.response;
            mediaType = foundIntent.mediaType;
            mediaSrc = foundIntent.mediaSrc;
        }

        escreverTexto(responseText);
        falarVoz(responseText);
        showMedia(mediaType, mediaSrc);
    }
}

// Event Listeners
btnEnviar.addEventListener('click', processInput);
inputTexto.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        processInput();
    }
});

// Initialization
window.addEventListener('DOMContentLoaded', () => {
    createUniverse();
    
    // Força o carregamento prévio das vozes no navegador
    if ('speechSynthesis' in window) {
        speechSynthesis.getVoices();
    }

    // Iniciar uma pequena mensagem de boas vindas automática após carregar
    setTimeout(() => {
        falarVoz("Sistemas inicializados. Bem-vindos à apresentação do Projeto Integrador.");
    }, 10000);
});