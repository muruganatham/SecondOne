import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Database, Download, Terminal } from 'lucide-react';
import '../App.css';

function ChatUI() {
    const [messages, setMessages] = useState([
        { sender: 'system', text: 'Hello! I am your Amypo Database Assistant. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/api/v1/ai/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ question: userMessage.text }),
            });

            const data = await response.json();

            if (data.answer) {
                setMessages(prev => [...prev, {
                    sender: 'ai',
                    text: data.answer,
                    sql: data.sql,
                    data: data.data
                }]);
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

    // Animation Variants
    const messageVariants = {
        hidden: { opacity: 0, y: 10 },
        visible: { opacity: 1, y: 0 }
    };

    return (
        <div className="chat-container">
            {messages.length <= 1 ? (
                <motion.div
                    className="chat-welcome"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                >
                    <div style={{
                        width: '80px', height: '80px', background: 'var(--primary-color)',
                        borderRadius: '24px', display: 'flex', alignItems: 'center',
                        justifyContent: 'center', marginBottom: '1.5rem', boxShadow: '0 10px 25px rgba(46, 139, 87, 0.2)'
                    }}>
                        <Bot size={40} color="white" />
                    </div>
                    <h1>Hello! I am your Amypo Database Assistant</h1>
                    <p>How can I help you today?</p>
                </motion.div>
            ) : (
                <div className="messages-area">
                    <AnimatePresence>
                        {messages.slice(1).map((msg, index) => ( // Skip initial greeting if we handle it differently or keep it
                            <motion.div
                                key={index}
                                className={`message-bubble ${msg.sender}`}
                                variants={messageVariants}
                                initial="hidden"
                                animate="visible"
                                style={{
                                    marginBottom: '20px',
                                    alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                                    maxWidth: '80%',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: msg.sender === 'user' ? 'flex-end' : 'flex-start'
                                }}
                            >
                                <div style={{ display: 'flex', gap: '15px', flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row' }}>
                                    <div className={`avatar`} style={{
                                        width: '36px', height: '36px', borderRadius: '12px',
                                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                                        flexShrink: 0,
                                        boxShadow: '0 4px 10px rgba(0,0,0,0.05)'
                                    }}>
                                        {msg.sender === 'user' ? <User size={18} /> : <Bot size={18} />}
                                    </div>
                                    <div className="message-content-box">
                                        {msg.text}
                                    </div>
                                </div>

                                {/* SQL Output Block */}
                                {msg.sql && (
                                    <motion.div
                                        initial={{ opacity: 0, height: 0 }}
                                        animate={{ opacity: 1, height: 'auto' }}
                                        className="sql-block"
                                        style={{ marginTop: '12px', width: '100%', maxWidth: '600px', marginLeft: msg.sender === 'user' ? 0 : '50px', marginRight: msg.sender === 'user' ? '50px' : 0 }}
                                    >
                                        <details className="sql-details" style={{ border: '1px solid var(--border)', borderRadius: '12px', overflow: 'hidden', background: 'var(--bg-primary)' }}>
                                            <summary style={{ background: 'var(--bg-secondary)', padding: '10px 15px', fontSize: '0.85rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 500, color: 'var(--text-primary)' }}>
                                                <Terminal size={14} color="var(--primary-color)" /> View Generated SQL Query
                                            </summary>
                                            <pre style={{ margin: 0, padding: '15px', background: '#0f172a', color: '#e2e8f0', fontSize: '0.85rem', overflowX: 'auto', fontFamily: 'var(--font-mono)' }}>
                                                {msg.sql}
                                            </pre>
                                        </details>
                                    </motion.div>
                                )}

                                {/* Data Download */}
                                {msg.data && msg.data.length > 0 && (
                                    <motion.div
                                        initial={{ opacity: 0, y: 5 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        style={{ marginTop: '10px', marginLeft: '50px', display: 'flex', alignItems: 'center', gap: '12px' }}
                                    >
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', color: 'var(--text-secondary)', background: 'white', padding: '6px 12px', borderRadius: '20px', border: '1px solid var(--border)' }}>
                                            <Database size={14} />
                                            {msg.data.length} records found
                                        </div>
                                        <button
                                            className="download-btn"
                                            style={{
                                                display: 'flex', alignItems: 'center', gap: '6px',
                                                padding: '6px 16px', fontSize: '0.85rem',
                                                background: 'var(--primary-color)', color: 'white',
                                                border: 'none',
                                                borderRadius: '20px', cursor: 'pointer',
                                                boxShadow: '0 4px 10px rgba(46, 139, 87, 0.2)'
                                            }}
                                            onClick={() => {
                                                const headers = Object.keys(msg.data[0]);
                                                const csvContent = [
                                                    headers.join(','),
                                                    ...msg.data.map(row => headers.map(header => JSON.stringify(row[header])).join(','))
                                                ].join('\n');
                                                const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                                                const link = document.createElement('a');
                                                const url = URL.createObjectURL(blob);
                                                link.setAttribute('href', url);
                                                link.setAttribute('download', 'query_result.csv');
                                                link.click();
                                            }}
                                        >
                                            <Download size={14} /> Download CSV
                                        </button>
                                    </motion.div>
                                )}
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    <div ref={messagesEndRef} />
                </div>
            )}

            <div className="chat-input-area" style={{ padding: '20px 0' }}>
                <div className="chat-input-wrapper">
                    <input
                        className="chat-input-field"
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Ask anything..."
                        disabled={isLoading}
                    />
                    <button
                        className="send-btn-floating"
                        onClick={sendMessage}
                        disabled={isLoading}
                    >
                        <Send size={20} />
                    </button>
                </div>
                <div style={{ textAlign: 'center', marginTop: '10px', fontSize: '0.8rem', color: '#94a3b8' }}>
                    AI can make mistakes. Please verify important information.
                </div>
            </div>
        </div>
    );
}

export default ChatUI;
