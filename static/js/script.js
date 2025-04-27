const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

function addMessage(content, className) {
    const msg = document.createElement('div');
    msg.className = className;
    msg.innerHTML = content;
    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user-message');
    userInput.value = '';
    sendBtn.disabled = true;
    sendBtn.textContent = 'Sending...';

    // Loading indicator
    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'bot-message loading';
    loadingMsg.textContent = 'Thinking...';
    chatContainer.appendChild(loadingMsg);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatContainer.removeChild(loadingMsg);
        animateBotReply(data.response);
    })
    .catch(error => {
        chatContainer.removeChild(loadingMsg);
        addMessage("Sorry, an error occurred!", 'bot-message');
    })
    .finally(() => {
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
    });
}

function animateBotReply(text) {
    const botMessage = document.createElement('div');
    botMessage.className = 'bot-message';
    chatContainer.appendChild(botMessage);

    let words = text.split(' ');
    let index = 0;

    function typeNextWord() {
        if (index < words.length) {
            botMessage.innerHTML += words[index] + ' ';
            index++;
            chatContainer.scrollTop = chatContainer.scrollHeight;
            setTimeout(typeNextWord, 50); // Typing speed (50ms per word)
        }
    }

    typeNextWord();
}
