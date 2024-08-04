
let socket;
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendButton = document.querySelector('#chat-form button[type="submit"]');

let isBotResponding = false;
let currentBotMessage = '';

function validateAPIKeyAndConnect(showSuccess = false) {
    fetch('/api/validate-openai-api-key', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.valid) {
            if (showSuccess) {
                showSuccessMessage();
            }
            connect();
        } else {
            showInvalidKeyPopup();
        }
    })
    .catch(error => {
        console.error('Error validating API key:', error);
    });
}

function showInvalidKeyPopup() {
    const popup = document.createElement('div');
    popup.id = 'invalid-key-popup';
    popup.innerHTML = `
        <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-white p-6 rounded shadow-md">
                <h2 class="text-xl font-semibold mb-4">Invalid API Key</h2>
                <p class="mb-4">Your OpenAI API key is invalid. Please update your .env file.</p>
                <div class="flex justify-center">
                    <button id="try-again-button" class="btn btn-primary">Try Again</button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(popup);

    document.getElementById('try-again-button').addEventListener('click', () => {
        document.body.removeChild(popup);
        validateAPIKeyAndConnect(true);
    });
}

function showSuccessMessage() {
    const successMessage = document.createElement('div');
    successMessage.className = 'alert alert-success fixed top-4 left-1/2 transform -translate-x-1/2 max-w-sm w-full';
    successMessage.innerHTML = `
        <div class="flex justify-center">
            <span>API key validated successfully!</span>
        </div>
    `;
    document.body.appendChild(successMessage);
    setTimeout(() => {
        document.body.removeChild(successMessage);
    }, 3000);
}

function connect() {
    socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = function(e) {
        console.log('WebSocket connection established');
        authenticate();
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleMessage(data);
    };

    socket.onclose = function(event) {
        console.log('WebSocket connection closed:', event);
    };

    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };
}

function authenticate() {
    const token = 'user_' + Math.random().toString(36).substr(2, 9);  // Simple dummy token generation
    socket.send(JSON.stringify({type: 'auth', token: token}));
    document.getElementById('chat-token-value').textContent = token;
}

function handleMessage(data) {
    switch(data.type) {
        case 'auth':
            console.log('Authentication status:', data.content);
            break;
        case 'stream':
            if (!isBotResponding) {
                isBotResponding = true;
                disableSendButton();
            }
            updateChatMessages(data.content, false, true);
            break;
        case 'end':
            finalizeBotMessage();
            isBotResponding = false;
            enableSendButton();
            break;
        case 'error':
            console.error('Error:', data.content);
            isBotResponding = false;
            enableSendButton();
            break;
    }
}

function updateChatMessages(message, isUser, isStreaming = false) {
    if (isUser) {
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('chat', 'chat-end', 'mb-4');
        userMessageElement.innerHTML = `
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="/static/imgs/user_icon.png" alt="User Avatar" />
                </div>
            </div>
            <div class="chat-bubble bg-slate-500">${message}</div>
        `;
        chatMessages.appendChild(userMessageElement);
    } else {
        let botMessageElement = chatMessages.querySelector('.chat-start:last-child');
        if (!botMessageElement || !isStreaming) {
            botMessageElement = document.createElement('div');
            botMessageElement.classList.add('chat', 'chat-start', 'mb-4');
            botMessageElement.innerHTML = `
                <div class="chat-image avatar">
                    <div class="w-10 rounded-full">
                        <img src="/static/imgs/ai_icon.png" alt="Bot Avatar" />
                    </div>
                </div>
                <div class="chat-bubble bg-slate-700"></div>
            `;
            chatMessages.appendChild(botMessageElement);
            currentBotMessage = '';
        }
        
        currentBotMessage += message;
        const chatBubble = botMessageElement.querySelector('.chat-bubble');
        chatBubble.innerHTML = marked.parse(currentBotMessage);
    }

    scrollToBottom();
}

function finalizeBotMessage() {
    const lastBotMessage = chatMessages.querySelector('.chat-start:last-child');
    if (lastBotMessage) {
        const chatBubble = lastBotMessage.querySelector('.chat-bubble');
        chatBubble.innerHTML = marked.parse(currentBotMessage);
        lastBotMessage.classList.remove('typing');
    }
    currentBotMessage = '';
    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function disableSendButton() {
    sendButton.disabled = true;
    sendButton.classList.add('opacity-50', 'cursor-not-allowed');
}

function enableSendButton() {
    sendButton.disabled = false;
    sendButton.classList.remove('opacity-50', 'cursor-not-allowed');
}

chatForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (message && !isBotResponding) {
        updateChatMessages(message, true);
        let msgHistoryLen = document.getElementById('chatHistoryLenSelect').value.trim()
        socket.send(JSON.stringify({type: 'message', message: message, max_msg_history_len: msgHistoryLen}));
        userInput.value = '';
    }
});

// Set initial scroll position
scrollToBottom();

// Make sure the chat container is scrollable
chatMessages.style.maxHeight = 'calc(100vh - 300px)';
chatMessages.style.overflowY = 'auto';

// Validate API key and connect
validateAPIKeyAndConnect();