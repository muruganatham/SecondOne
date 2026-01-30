import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Lightbulb, Download, Terminal } from 'lucide-react';
import ChatSidebar from '../components/ChatSidebar';
import DataVisualization from '../components/DataVisualization';
import ConfirmationModal from '../components/ConfirmationModal';
import { conversationService } from '../services/conversationService';

function ChatUI() {
    // Conversation Management
    const [conversations, setConversations] = useState([]);
    const [activeConversationId, setActiveConversationId] = useState(null);

    // Current Chat State
    const [messages, setMessages] = useState([
        { sender: 'system', text: 'Hello! I am your Amypo Database Assistant' },
        { sender: 'ai', text: 'Hello! How can I assist you today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [followUpQuestions, setFollowUpQuestions] = useState([]);

    // Confirmation Modal State
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [pendingQuery, setPendingQuery] = useState(null);

    const messagesEndRef = useRef(null);

    // Load conversations from backend API on mount
    useEffect(() => {
        const fetchConversations = async () => {
            try {
                const data = await conversationService.getAll();
                setConversations(data);
                if (data.length > 0) {
                    setActiveConversationId(data[0].id);
                    setMessages(data[0].messages);
                }
            } catch (error) {
                console.error('Error fetching conversations:', error);
            }
        };
        fetchConversations();
    }, []);

    // Check for new chat trigger from Dashboard
    useEffect(() => {
        const createNewChat = localStorage.getItem('createNewChat');
        if (createNewChat === 'true') {
            localStorage.removeItem('createNewChat');
            handleNewChat();
        }
    }, []);

    // Auto-scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Keyboard Shortcuts
    useEffect(() => {
        const handleKeyDown = (e) => {
            // Ctrl+N for new chat
            if (e.ctrlKey && e.key === 'n') {
                e.preventDefault();
                handleNewChat();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, []);

    // Save current conversation to backend
    const saveConversation = async (updatedMessages) => {
        try {
            if (activeConversationId) {
                // Update existing conversation
                const updated = await conversationService.update(activeConversationId, {
                    messages: updatedMessages
                });
                setConversations(prev => prev.map(conv =>
                    conv.id === activeConversationId ? updated : conv
                ));
            } else {
                // Create new conversation
                const newConv = await conversationService.create({
                    title: updatedMessages[1]?.text.substring(0, 50) || 'New Chat',
                    messages: updatedMessages
                });
                setConversations(prev => [newConv, ...prev]);
                setActiveConversationId(newConv.id);
            }
        } catch (error) {
            console.error('Error saving conversation:', error);
        }
    };

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: 'user', text: input };
        const updatedMessages = [...messages, userMessage];
        setMessages(updatedMessages);
        setInput('');
        setIsLoading(true);
        setFollowUpQuestions([]);

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

            // Check if query requires confirmation
            if (data.requires_confirmation && !pendingQuery) {
                // Store the query for confirmation
                setPendingQuery({
                    userMessage,
                    updatedMessages,
                    data
                });
                setShowConfirmation(true);
                setIsLoading(false);
                return; // Wait for user confirmation
            }

            if (data.answer) {
                const aiMessage = {
                    sender: 'ai',
                    text: data.answer,
                    sql: data.sql,
                    data: data.data
                };
                const finalMessages = [...updatedMessages, aiMessage];
                setMessages(finalMessages);
                saveConversation(finalMessages);

                // Use AI-generated follow-ups from API
                if (data.follow_ups && data.follow_ups.length > 0) {
                    setFollowUpQuestions(data.follow_ups);
                } else {
                    // Fallback to generic suggestions
                    setFollowUpQuestions([
                        "Can you show me more details?",
                        "How does this compare to other records?",
                        "What are the trends over time?"
                    ]);
                }
            } else {
                const errorMessage = { sender: 'system', text: 'Received unexpected response from server.' };
                const finalMessages = [...updatedMessages, errorMessage];
                setMessages(finalMessages);
                saveConversation(finalMessages);
            }

        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = { sender: 'system', text: 'Error connecting to the server. Please ensure the backend is running.' };
            const finalMessages = [...updatedMessages, errorMessage];
            setMessages(finalMessages);
            saveConversation(finalMessages);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFollowUpClick = (question) => {
        setInput(question);
    };

    const handleNewChat = () => {
        setActiveConversationId(null);
        setMessages([
            { sender: 'system', text: 'Hello! I am your Amypo Database Assistant. How can I help you today?' },
            { sender: 'ai', text: 'Hello! How can I assist you today? Feel free to ask me anything about your database - I can help you query data, analyze information, or answer questions about your stored records.' }
        ]);
        setFollowUpQuestions([]);
    };

    const handleSelectConversation = (id) => {
        const conv = conversations.find(c => c.id === id);
        if (conv) {
            setActiveConversationId(id);
            setMessages(conv.messages);
            setFollowUpQuestions([]);
        }
    };

    const handleDeleteConversation = async (id) => {
        try {
            await conversationService.delete(id);
            setConversations(prev => prev.filter(c => c.id !== id));
            if (activeConversationId === id) {
                handleNewChat();
            }
        } catch (error) {
            console.error('Error deleting conversation:', error);
        }
    };

    // Export Chat as TXT
    const exportChat = () => {
        const chatText = messages
            .filter(m => m.sender !== 'system')
            .map(m => `${m.sender.toUpperCase()}: ${m.text}${m.sql ? '\n\nSQL: ' + m.sql : ''}`)
            .join('\n\n---\n\n');

        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-${new Date().toISOString().slice(0, 10)}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    };

    // Confirmation Handlers
    const handleConfirm = () => {
        if (pendingQuery) {
            const { data, updatedMessages } = pendingQuery;

            // Process the confirmed query
            const aiMessage = {
                sender: 'ai',
                text: data.answer,
                sql: data.sql,
                data: data.data
            };
            const finalMessages = [...updatedMessages, aiMessage];
            setMessages(finalMessages);
            saveConversation(finalMessages);

            // Set follow-ups
            if (data.follow_ups && data.follow_ups.length > 0) {
                setFollowUpQuestions(data.follow_ups);
            }

            // Clear pending query and close modal
            setPendingQuery(null);
            setShowConfirmation(false);
        }
    };

    const handleCancel = () => {
        // Clear pending query and close modal
        setPendingQuery(null);
        setShowConfirmation(false);

        // Add cancellation message
        if (pendingQuery) {
            const cancelMessage = {
                sender: 'system',
                text: 'Query cancelled. The database was not modified.'
            };
            const finalMessages = [...pendingQuery.updatedMessages, cancelMessage];
            setMessages(finalMessages);
            saveConversation(finalMessages);
        }
    };

    return (
        <div className="flex w-full h-full relative overflow-hidden">
            {/* Confirmation Modal */}
            <ConfirmationModal
                isOpen={showConfirmation}
                onClose={handleCancel}
                onConfirm={handleConfirm}
                sql={pendingQuery?.data?.sql || ''}
                affectedRows={pendingQuery?.data?.affected_rows || 0}
            />

            <ChatSidebar
                conversations={conversations}
                activeConversationId={activeConversationId}
                onSelectConversation={handleSelectConversation}
                onNewChat={handleNewChat}
                onDeleteConversation={handleDeleteConversation}
            />

            {/* Main Chat Area - Full Width */}
            <div className="flex-1 flex flex-col h-full bg-slate-50/50 relative ml-16 peer-[.expanded]:ml-72 transition-all duration-300 ease-in-out">

                {/* Export Button */}
                {messages.length > 1 && (
                    <button
                        onClick={exportChat}
                        className="absolute top-4 right-6 px-4 py-2.5 bg-gradient-to-br from-purple-500 to-pink-500 text-white rounded-xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:-translate-y-0.5 transition-all z-20 flex items-center gap-2 font-medium text-sm"
                        title="Export chat as TXT"
                    >
                        <Download size={16} />
                        Export
                    </button>
                )}

                {messages.length <= 1 ? (
                    <motion.div
                        className="flex-1 flex flex-col items-center justify-center text-center p-8 w-full"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                    >
                        <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-3xl flex items-center justify-center mb-6 shadow-xl shadow-purple-500/20">
                            <Bot size={40} className="text-white" />
                        </div>
                        <h1 className="text-3xl font-bold text-slate-800 mb-2">Hello! I am your Amypo Database Assistant</h1>
                        <p className="text-slate-500 text-lg">How can I help you today?</p>
                        <div className="mt-8 text-sm text-slate-400">
                            <kbd className="bg-white/50 px-2 py-1 rounded text-slate-600 font-mono text-xs mx-1 border border-slate-200">Ctrl+N</kbd> New chat
                        </div>
                    </motion.div>
                ) : (
                    <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6 scroll-smooth w-full">
                        <AnimatePresence>
                            {messages.slice(1).map((msg, index) => (
                                <motion.div
                                    key={index}
                                    className={`flex items-start gap-4 w-full ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                >
                                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-sm ${msg.sender === 'user' ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white' : 'bg-white text-purple-600 border border-purple-100'}`}>
                                        {msg.sender === 'user' ? <User size={20} /> : <Bot size={20} />}
                                    </div>

                                    <div className="flex-1 min-w-0 max-w-4xl">
                                        <div className={`p-4 rounded-2xl text-[15px] leading-relaxed shadow-sm ${msg.sender === 'user' ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white' : 'bg-white text-slate-800 border border-slate-100'}`}>
                                            {msg.text}
                                        </div>

                                        {/* SQL Block */}
                                        {msg.sql && (
                                            <motion.details
                                                className="mt-3 border border-purple-200 rounded-xl overflow-hidden bg-white/50 backdrop-blur-sm"
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                            >
                                                <summary className="bg-purple-50 p-3 text-sm cursor-pointer flex items-center gap-2 font-medium text-purple-700 hover:bg-purple-100 transition-colors select-none">
                                                    <Terminal size={14} className="text-purple-600" />
                                                    View Generated SQL Query
                                                </summary>
                                                <pre className="p-4 m-0 text-xs bg-slate-800 text-slate-200 overflow-x-auto font-mono custom-scrollbar">
                                                    {msg.sql}
                                                </pre>
                                            </motion.details>
                                        )}

                                        {/* Data Visualization */}
                                        {msg.data && msg.data.length > 0 && (
                                            <div className="mt-4">
                                                <DataVisualization
                                                    data={msg.data}
                                                    sql={msg.sql}
                                                />
                                            </div>
                                        )}

                                        {/* Follow-up Questions */}
                                        {msg.sender === 'ai' && index === messages.length - 2 && followUpQuestions.length > 0 && (
                                            <motion.div
                                                className="mt-4 ml-1"
                                                initial={{ opacity: 0, y: 10 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: 0.3 }}
                                            >
                                                <div className="flex items-center gap-2 text-xs font-semibold text-purple-400 uppercase tracking-wider mb-2">
                                                    <Lightbulb size={14} />
                                                    <span>Suggested follow-ups</span>
                                                </div>
                                                <div className="flex flex-wrap gap-2">
                                                    {followUpQuestions.map((q, i) => (
                                                        <button
                                                            key={i}
                                                            onClick={() => handleFollowUpClick(q)}
                                                            className="px-4 py-2 bg-white border border-purple-200 rounded-xl text-sm text-slate-600 hover:border-purple-400 hover:text-purple-600 hover:bg-purple-50 transition-all text-left"
                                                        >
                                                            {q}
                                                        </button>
                                                    ))}
                                                </div>
                                            </motion.div>
                                        )}
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                        <div ref={messagesEndRef} />
                    </div>
                )}

                {/* Input Area - Full Width */}
                <div className="px-6 py-4 bg-white/80 backdrop-blur-md border-t border-purple-100 sticky bottom-0 z-10 w-full">
                    <div className="w-full relative bg-white border border-purple-200 rounded-2xl flex items-center p-2 focus-within:ring-2 focus-within:ring-purple-300 focus-within:border-purple-400 transition-all shadow-sm">
                        <input
                            className="flex-1 bg-transparent border-none outline-none text-slate-800 px-4 py-3 placeholder-slate-400 min-w-0"
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                            placeholder="Ask anything about your database..."
                            disabled={isLoading}
                        />
                        <button
                            onClick={sendMessage}
                            disabled={isLoading || !input.trim()}
                            className="p-3 bg-gradient-to-br from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 font-medium shrink-0 shadow-lg shadow-purple-500/30"
                        >
                            <Send size={18} />
                            <span className="hidden sm:inline">{isLoading ? 'Sending...' : 'Send'}</span>
                        </button>
                    </div>
                    <div className="text-center mt-3 text-xs text-slate-400">
                        AI can make mistakes. Please verify important information.
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ChatUI;
