import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

function ChatUI() {
    const [messages, setMessages] = useState([
        { sender: 'system', text: 'Hello! Ask me anything about your database.' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/v1/ai/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: userMessage.text }),
            });

            const data = await response.json();

            if (data.answer) {
                setMessages(prev => [...prev, { sender: 'ai', text: data.answer, sql: data.sql, data: data.data }]);
            } else {
                setMessages(prev => [...prev, { sender: 'system', text: 'Received unexpected response from server.' }]);
            }

        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, { sender: 'system', text: 'Error connecting to the server. Please ensure the backend is running.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h2>Amypo Database Assistant</h2>
            </div>

            <div className="messages-area">
                {/* Initial System Message */}
                <div className="message system">
                    <div className="message-prefix">AMYPO SYSTEM</div>
                    <div className="message-text">Welcome. I am ready to assist you with database queries.</div>
                </div>

                {messages.slice(1).map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        <div className="message-prefix">
                            {msg.sender === 'user' ? 'YOU' : 'AMYPO ASSISTANT'}
                        </div>
                        <div className="message-text">{msg.text}</div>

                        {/* SQL Output */}
                        {msg.sql && (
                            <details className="sql-details">
                                <summary>View Generated SQL</summary>
                                <pre>{msg.sql}</pre>
                            </details>
                        )}

                        {/* CSV Download for Large Data */}
                        {msg.data && msg.data.length > 25 && (
                            <div className="data-download-container">
                                <p>
                                    Found <strong>{msg.data.length}</strong> records.
                                </p>
                                <button
                                    onClick={() => {
                                        const headers = Object.keys(msg.data[0]);
                                        const csvContent = [
                                            headers.join(','),
                                            ...msg.data.map(row => headers.map(header => JSON.stringify(row[header])).join(','))
                                        ].join('\n');

                                        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                                        const link = document.createElement('a');
                                        if (link.download !== undefined) {
                                            const url = URL.createObjectURL(blob);
                                            link.setAttribute('href', url);
                                            link.setAttribute('download', 'query_result.csv');
                                            link.style.visibility = 'hidden';
                                            document.body.appendChild(link);
                                            link.click();
                                            document.body.removeChild(link);
                                        }
                                    }}
                                >
                                    Download CSV
                                </button>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <div className="input-section">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask a question about your data..."
                    disabled={isLoading}
                    className="chat-input"
                    autoFocus
                />
                <button onClick={sendMessage} disabled={isLoading} className="send-button">
                    {isLoading ? 'Processing...' : 'Send Query'}
                </button>
            </div>
        </div>
    );
}

export default ChatUI;
