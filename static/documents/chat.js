document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const modal = document.getElementById('info-modal');
    const closeModal = document.querySelector('.close-button');
    const modalSources = document.getElementById('modal-sources');
    const modalPrompt = document.getElementById('modal-prompt');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = messageInput.value.trim();
        if (!question) return;

        addMessage(question, 'user');
        messageInput.value = '';

        const loadingMessage = addMessage('<span></span><span></span><span></span>', 'loading');
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const response = await fetch('/api/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ question: question }),
            });

            chatMessages.removeChild(loadingMessage);

            if (!response.ok) {
                addMessage('خطا در ارتباط با سرور.', 'bot');
                return;
            }

            const data = await response.json();
            addBotMessage(data);

        } catch (error) {
            chatMessages.removeChild(loadingMessage);
            addMessage('یک خطای غیرمنتظره رخ داد.', 'bot');
        }
    });

    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerHTML = text; // اینجا همون text میمونه
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageDiv;
    }

    function addBotMessage(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        
        // تبدیل مارک‌داون به HTML برای جواب‌های هوش مصنوعی
        messageDiv.innerHTML = marked.parse(data.answer);

        if (data.sources && data.sources.length > 0) {
            const infoButton = document.createElement('button');
            infoButton.className = 'info-button';
            infoButton.innerText = 'i';
            infoButton.onclick = () => showInfoModal(data.sources, data.prompt);
            messageDiv.appendChild(infoButton);
        }

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showInfoModal(sources, prompt) {
        modalSources.innerHTML = '';
        sources.forEach(source => {
            const li = document.createElement('li');
            li.textContent = source;
            modalSources.appendChild(li);
        });

        modalPrompt.textContent = prompt;
        modal.style.display = 'flex';
    }

    closeModal.onclick = () => {
        modal.style.display = 'none';
    };

    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
    
    // Function to get CSRF token for POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});