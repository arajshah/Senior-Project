document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const messages = document.getElementById('messages');
    const submitButton = document.querySelector('#chat-form button');

    form.addEventListener('submit', handleSubmit);
    submitButton.addEventListener('click', handleSubmit);

    async function handleSubmit(e) {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        // Disable input and button while processing
        input.disabled = true;
        submitButton.disabled = true;

        // Add user message
        const userDiv = createMessageElement(message, 'user');
        messages.appendChild(userDiv);
        messages.scrollTop = messages.scrollHeight;
        input.value = '';

        // Create placeholder for assistant response
        const assistantDiv = createMessageElement('', 'assistant');
        messages.appendChild(assistantDiv);
        const messageBubble = assistantDiv.querySelector('.message-bubble');
        messageBubble.classList.add('typing');

        try {
            const response = await fetch('/api/chat/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let responseText = '';

            while (true) {
                const {value, done} = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            responseText += data.chunk;
                            messageBubble.textContent = responseText;
                            messages.scrollTop = messages.scrollHeight;
                        } catch (e) {
                            console.error('Error parsing JSON:', e);
                        }
                    }
                }
            }
            messageBubble.classList.remove('typing');
        } catch (error) {
            console.error('Error:', error);
            messageBubble.textContent = 'Sorry, I encountered an error. Please try again.';
            messageBubble.classList.remove('typing');
        } finally {
            // Re-enable input and button
            input.disabled = false;
            submitButton.disabled = false;
            input.focus();
        }
    }

    function createMessageElement(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                ${type === 'assistant' ? '<i class="fas fa-moon message-icon"></i>' : ''}
                <div class="message-bubble">${text}</div>
            </div>
            <div class="message-time">${time}</div>
        `;

        return messageDiv;
    }
});