import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Lightbulb, Download, Terminal, Brain, Cpu, Square } from 'lucide-react';
import ChatSidebar from '../Components/ChatSidebar';
import DataVisualization from '../Components/DataVisualization';
import ConfirmationModal from '../Components/ConfirmationModal';
import { conversationService } from '../services/conversationService';
import logo from '../assets/logo.png'; // Make sure this path is correct
import headerLogo from '../assets/header_logo.png';

function ChatUI() {
    // Conversation Management
    const [conversations, setConversations] = useState([]);
    const [activeConversationId, setActiveConversationId] = useState(null);

    // Current Chat State
    const [selectedModel, setSelectedModel] = useState('deepseek-chat');
    const [messages, setMessages] = useState([
        { sender: 'system', text: 'Hello! I am your Amypo Database Assistant' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [followUpQuestions, setFollowUpQuestions] = useState([]);

    // Confirmation Modal State
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [pendingQuery, setPendingQuery] = useState(null);

    const messagesEndRef = useRef(null);
    const messagesContainerRef = useRef(null);

    // Load conversations from backend API on mount
    useEffect(() => {
        const fetchConversations = async () => {
            try {
                const data = await conversationService.getAll();
                // Ensure data is an array before using it
                if (Array.isArray(data)) {
                    setConversations(data);
                    if (data.length > 0) {
                        setActiveConversationId(data[0].id);
                        setMessages(data[0].messages);
                    }
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

    // ChatGPT-style auto-scroll: Always scroll to bottom on new messages
    const scrollToBottom = () => {
        setTimeout(() => {
            if (messagesContainerRef.current) {
                messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
            }
        }, 100);
    };

    // Auto-scroll on messages change (like ChatGPT)
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
            // Filter out system messages and the initial greeting
            const messagesToSave = updatedMessages.filter(msg =>
                msg.sender !== 'system' &&
                !(msg.sender === 'ai' && msg.text === 'Hello! How can I assist you today?' && !msg.sql)
            );

            // Don't save if there are no real messages
            if (messagesToSave.length === 0) return;

            // Format messages to match backend schema - ensure all fields are present
            const formattedMessages = messagesToSave.map(msg => ({
                sender: msg.sender,
                text: msg.text,
                sql: msg.sql || null,
                data: msg.data || null
            }));

            if (activeConversationId) {
                // Update existing conversation
                const updated = await conversationService.update(activeConversationId, {
                    messages: formattedMessages
                });
                setConversations(prev => prev.map(conv =>
                    conv.id === activeConversationId ? updated : conv
                ));
            } else {
                // Create new conversation - use first user message for title
                const firstUserMsg = messagesToSave.find(m => m.sender === 'user');
                const newConv = await conversationService.create({
                    title: firstUserMsg?.text.substring(0, 50) || 'New Chat',
                    messages: formattedMessages
                });
                setConversations(prev => [newConv, ...prev]);
                setActiveConversationId(newConv.id);
            }
        } catch (error) {
            console.error('Error saving conversation:', error);
        }
    };

    const abortControllerRef = useRef(null);

    const stopGeneration = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            abortControllerRef.current = null;
            setIsLoading(false);
        }
    };

    const sendMessage = async () => {
        if (isLoading) {
            stopGeneration();
            return;
        }

        if (!input.trim()) return;

        // Abort previous if any
        if (abortControllerRef.current) abortControllerRef.current.abort();
        abortControllerRef.current = new AbortController();

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
                body: JSON.stringify({ question: input }),
                signal: abortControllerRef.current.signal
            });

            const data = await response.json();

            if (data.requires_confirmation) {
                setPendingQuery({ query: input, data });
                setShowConfirmation(true);
                setIsLoading(false);
                return;
            }

            const aiMessage = {
                sender: 'ai',
                text: data.answer,
                sql: data.sql,
                data: data.data || []
            };

            const finalMessages = [...updatedMessages, aiMessage];
            setMessages(finalMessages);
            setFollowUpQuestions(data.follow_ups || []);
            await saveConversation(finalMessages);

        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('Fetch aborted');
                setMessages([...updatedMessages, { sender: 'system', text: '🛑 Request cancelled by user.' }]);
                return;
            }
            console.error('Error:', error);
            const errorMessage = {
                sender: 'ai',
                text: 'Sorry, there was an error processing your request.'
            };
            const finalMessages = [...updatedMessages, errorMessage];
            setMessages(finalMessages);
        } finally {
            setIsLoading(false);
            abortControllerRef.current = null;
        }
    };

    const handleConfirm = async () => {
        setShowConfirmation(false);
        setIsLoading(true);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/api/v1/ai/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    question: pendingQuery.query,
                    confirmed: true
                }),
            });

            const data = await response.json();
            const aiMessage = {
                sender: 'ai',
                text: data.answer,
                sql: data.sql,
                data: data.data || []
            };

            const finalMessages = [...messages, aiMessage];
            setMessages(finalMessages);
            setFollowUpQuestions(data.follow_ups || []);
            await saveConversation(finalMessages);

        } catch (error) {
            console.error('Error:', error);
        } finally {
            setIsLoading(false);
            setPendingQuery(null);
        }
    };

    const handleCancel = () => {
        setShowConfirmation(false);
        setPendingQuery(null);
        setIsLoading(false);
    };

    const handleFollowUpClick = (question) => {
        setInput(question);
    };

    const handleNewChat = () => {
        setMessages([
            { sender: 'system', text: 'Hello! I am your Amypo Database Assistant' }
        ]);
        setActiveConversationId(null);
        setFollowUpQuestions([]);
    };

    const handleSelectConversation = (conversation) => {
        setActiveConversationId(conversation.id);
        setMessages(conversation.messages || []);
        setFollowUpQuestions([]);
    };

    const handleDeleteConversation = async (conversationId) => {
        try {
            await conversationService.delete(conversationId);
            setConversations(prev => {
                const newConversations = prev.filter(conv => conv.id !== conversationId);
                return [...newConversations]; // Create a new array reference to force re-render
            });
            if (conversationId === activeConversationId) {
                handleNewChat();
            }
        } catch (error) {
            console.error('Error deleting conversation:', error);
        }
    };

    const exportChat = () => {
        const chatText = messages
            .filter(msg => msg.sender !== 'system')
            .map(msg => `${msg.sender === 'user' ? 'You' : 'AI'}: ${msg.text}`)
            .join('\n\n');

        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="flex w-full items-center justify-center h-screen overflow-hidden">
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

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col h-screen ml-16 peer-[.expanded]:ml-56 transition-all duration-300 overflow-hidden relative">

                {/* Fixed Header */}
                <div className="absolute top-0 left-0 right-0 z-10 px-6 py-4 bg-white/80 backdrop-blur-md border-b border-slate-100 flex items-center gap-3">
                    <img src={headerLogo} alt="Amypo Logo" className="w-8 h-8 object-contain" />
                    <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                        Amypo Assistant
                    </h1>
                </div>

                {/* Top Right Controls */}
                <div className="absolute top-4 right-6 z-20 flex items-center gap-3">
                    {/* Model Selector */}
                    <div className="relative group">
                        <button className="flex items-center gap-2 px-3 py-2 bg-white/80 backdrop-blur-sm rounded-xl border border-slate-200 hover:bg-slate-50 transition-all text-sm font-medium text-slate-700 shadow-sm">
                            {selectedModel === 'deepseek-chat' ? (
                                <>
                                    <Brain size={16} className="text-emerald-600" />
                                    <span>DeepSeek</span>
                                </>
                            ) : (
                                <>
                                    <Cpu size={16} className="text-blue-600" />
                                    <span>GPT-4</span>
                                </>
                            )}
                        </button>

                        {/* Dropdown */}
                        <div className="absolute top-full right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-slate-100 py-1 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all transform origin-top-right">
                            <button
                                onClick={() => setSelectedModel('deepseek-chat')}
                                className={`w-full text-left px-4 py-2.5 text-sm flex items-center gap-3 hover:bg-emerald-50 transition-colors ${selectedModel === 'deepseek-chat' ? 'text-emerald-700 font-medium bg-emerald-50/50' : 'text-slate-600'}`}
                            >
                                <Brain size={16} className="text-emerald-600" />
                                <div>
                                    <div className="font-medium">DeepSeek Chat</div>
                                    <div className="text-[10px] text-slate-400">Optimized for Coding</div>
                                </div>
                            </button>
                            <button
                                onClick={() => setSelectedModel('gpt-4')}
                                className={`w-full text-left px-4 py-2.5 text-sm flex items-center gap-3 hover:bg-blue-50 transition-colors ${selectedModel === 'gpt-4' ? 'text-blue-700 font-medium bg-blue-50/50' : 'text-slate-600'}`}
                            >
                                <Cpu size={16} className="text-blue-600" />
                                <div>
                                    <div className="font-medium">GPT-4</div>
                                    <div className="text-[10px] text-slate-400">Advanced Reasoning</div>
                                </div>
                            </button>
                        </div>
                    </div>

                    {/* Export Button */}
                    {messages.length > 1 && (
                        <motion.button
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            onClick={exportChat}
                            className="px-4 py-2 bg-white/80 backdrop-blur-sm text-emerald-600 rounded-xl border border-emerald-200 hover:bg-emerald-50 hover:border-emerald-300 transition-all flex items-center gap-2 font-medium text-sm shadow-sm hover:shadow-md"
                            title="Export chat as TXT"
                        >
                            <Download size={16} />
                            <span className="hidden sm:inline">Export</span>
                        </motion.button>
                    )}
                </div>

                {/* Messages Area */}
                <div className="flex-1 flex flex-col overflow-hidden pt-16">
                    <div className='flex-1 overflow-hidden flex items-center justify-center'>
                        <div className="w-[800px] h-full flex flex-col">
                            {messages.length <= 1 ? (
                                <motion.div

                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ duration: 0.4 }}
                                    className="flex flex-col items-center justify-center h-full"
                                >
                                    {/* Gradient Bot Icon */}
                                    <motion.div
                                        className="relative mb-8 flex items-center justify-center"
                                        initial={{ scale: 0.8, opacity: 0 }}
                                        animate={{ scale: 1, opacity: 1 }}
                                        transition={{ delay: 0.1, duration: 0.5 }}
                                    >
                                        <div className="w-32 h-32 bg-white rounded-3xl flex items-center justify-center shadow-2xl shadow-emerald-500/20 relative border-4 border-emerald-100">
                                            <img src="/logo.png" alt="Amypo Logo" className="w-24 h-24 object-contain" />
                                        </div>
                                    </motion.div>

                                    {/* Welcome Text */}
                                    <motion.h1
                                        className="text-4xl text-center font-bold text-emerald-700 mb-3"
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.2 }}
                                    >
                                        Amypo Database Assistant
                                    </motion.h1>
                                    <motion.p
                                        className="text-lg text-center text-slate-600 mb-8"
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.3 }}
                                    >
                                        {/* Ask me anything about your student database using natural language */}
                                    </motion.p>
                                </motion.div>
                            ) : (
                                <div ref={messagesContainerRef} className="flex-1 overflow-y-auto py-6 min-h-0 scrollbar-hide pb-32">
                                    <div className="max-w-5xl mx-auto px-4 space-y-6">
                                        <AnimatePresence>
                                            {(Array.isArray(messages) ? messages : []).slice(1).map((msg, index) => (
                                                <motion.div
                                                    key={index}
                                                    className={`flex items-start gap-3 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}
                                                    initial={{ opacity: 0, y: 20 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    transition={{ duration: 0.3 }}
                                                >
                                                    {/* Avatar */}
                                                    <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 shadow-md overflow-hidden ${msg.sender === 'user'
                                                        ? 'bg-emerald-600 text-white'
                                                        : 'bg-white border-2 border-emerald-100 p-1'
                                                        }`}>
                                                        {msg.sender === 'user' ? (
                                                            <User size={20} strokeWidth={2.5} />
                                                        ) : (
                                                            <img src={logo} alt="AI" className="w-full h-full object-contain" />
                                                        )}
                                                    </div>

                                                    <div className="flex-1 min-w-0 w-full">
                                                        {/* Message Bubble */}
                                                        <div className={`p-5 rounded-2xl text-[15px] leading-relaxed ${msg.sender === 'user'
                                                            ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white shadow-lg shadow-purple-500/30'
                                                            : 'bg-white text-slate-800 border border-slate-200 shadow-sm'
                                                            }`}>
                                                            {msg.text}
                                                        </div>

                                                        {/* SQL Query Block - Hide if it's a dummy greeting query */}
                                                        {msg.sql && !msg.sql.includes("SELECT 'Hello'") && !msg.sql.includes("SELECT 'Knowledge Query'") && (
                                                            <motion.details
                                                                className="mt-4 border border-emerald-200 rounded-xl overflow-hidden bg-white shadow-sm"
                                                                initial={{ opacity: 0, y: 10 }}
                                                                animate={{ opacity: 1, y: 0 }}
                                                                transition={{ delay: 0.2 }}
                                                            >
                                                                <summary className="bg-emerald-50 px-4 py-3 cursor-pointer flex items-center gap-2 font-semibold text-emerald-700 hover:bg-emerald-100 transition-all select-none">
                                                                    <Terminal size={16} className="text-emerald-600" />
                                                                    <span className="text-sm">View Generated SQL Query</span>
                                                                </summary>
                                                                <pre className="p-4 m-0 text-xs bg-slate-900 text-slate-100 overflow-x-auto font-mono">
                                                                    {msg.sql}
                                                                </pre>
                                                            </motion.details>
                                                        )}

                                                        {/* Data Visualization - Hide for general conversation */}
                                                        {msg.data && Array.isArray(msg.data) && msg.data.length > 0 && (!msg.sql || (!msg.sql.includes("SELECT 'Hello'") && !msg.sql.includes("SELECT 'Knowledge Query'"))) && (
                                                            <motion.div
                                                                className="mt-4"
                                                                initial={{ opacity: 0, y: 10 }}
                                                                animate={{ opacity: 1, y: 0 }}
                                                                transition={{ delay: 0.3 }}
                                                            >
                                                                <DataVisualization data={msg.data} sql={msg.sql} />
                                                            </motion.div>
                                                        )}

                                                        {/* Follow-up Questions */}
                                                        {msg.sender === 'ai' && index === messages.length - 1 && followUpQuestions.length > 0 && (
                                                            <motion.div
                                                                className="mt-5"
                                                                initial={{ opacity: 0, y: 10 }}
                                                                animate={{ opacity: 1, y: 0 }}
                                                                transition={{ delay: 0.4 }}
                                                            >
                                                                <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 uppercase tracking-wider mb-3">
                                                                    <Lightbulb size={14} />
                                                                    <span>Suggested Questions</span>
                                                                </div>
                                                                <div className="flex flex-wrap gap-2">
                                                                    {followUpQuestions.map((q, i) => (
                                                                        <motion.button
                                                                            key={i}
                                                                            onClick={() => handleFollowUpClick(q)}
                                                                            className="px-4 py-2.5 bg-white border-2 border-emerald-200 rounded-xl text-sm text-slate-700 hover:border-emerald-400 hover:bg-emerald-50 hover:text-emerald-700 transition-all font-medium"
                                                                            whileHover={{ scale: 1.05 }}
                                                                            whileTap={{ scale: 0.95 }}
                                                                        >
                                                                            {q}
                                                                        </motion.button>
                                                                    ))}
                                                                </div>
                                                            </motion.div>
                                                        )}
                                                    </div>
                                                </motion.div>
                                            ))}
                                        </AnimatePresence>

                                        {/* Loading Indicator */}
                                        {isLoading && (
                                            <motion.div
                                                className="flex items-start gap-4"
                                                initial={{ opacity: 0, y: 20 }}
                                                animate={{ opacity: 1, y: 0 }}
                                            >
                                                <div className="w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 bg-white text-emerald-600 border-2 border-emerald-100 shadow-md">
                                                    <Bot size={20} strokeWidth={2.5} />
                                                </div>
                                                <div className="flex-1 max-w-3xl">
                                                    <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm">
                                                        <div className="flex items-center gap-2">
                                                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </motion.div>
                                        )}
                                    </div>

                                    <div ref={messagesEndRef} />
                                </div>
                            )}

                            {/* Input Area */}
                            <div className="py-3 bg-white/80 backdrop-blur-xl border-t border-emerald-100/50 sticky bottom-0">
                                <div className="max-w-5xl mx-auto px-4">
                                    <div className="relative bg-white border-2 border-emerald-200 rounded-2xl flex items-center p-1.5 focus-within:border-emerald-400 focus-within:shadow-lg focus-within:shadow-emerald-500/20 transition-all">
                                        <input
                                            className="flex-1 bg-transparent border-none outline-none text-slate-800 px-4 py-3.5 placeholder-slate-400 text-[15px]"
                                            type="text"
                                            value={input}
                                            onChange={(e) => setInput(e.target.value)}
                                            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                                            onFocus={() => {
                                                // Show AI greeting when user clicks input for the first time
                                                if (messages.length === 1) {
                                                    const aiGreeting = { sender: 'ai', text: 'Hello! How can I assist you today?' };
                                                    setMessages([...messages, aiGreeting]);
                                                }
                                            }}
                                            placeholder="Ask anything about your database..."
                                            disabled={isLoading}
                                        />
                                        <motion.button
                                            onClick={isLoading ? stopGeneration : sendMessage}
                                            disabled={!isLoading && !input.trim()}
                                            className={`px-5 py-3 rounded-xl transition-all flex items-center gap-2 font-semibold shadow-lg disabled:shadow-none ${isLoading
                                                ? 'bg-red-500 text-white hover:bg-red-600 shadow-red-500/30'
                                                : 'bg-emerald-600 text-white hover:bg-emerald-700 shadow-emerald-500/30 disabled:opacity-50 disabled:cursor-not-allowed'
                                                }`}
                                            whileHover={{ scale: 1.02 }}
                                            whileTap={{ scale: 0.98 }}
                                        >
                                            {isLoading ? <Square size={18} fill="currentColor" /> : <Send size={18} strokeWidth={2.5} />}
                                            <span className="hidden sm:inline">{isLoading ? 'Stop' : 'Send'}</span>
                                        </motion.button>
                                    </div>
                                    <p className="text-center mt-3 text-xs text-slate-400">
                                        AI can make mistakes. Please verify important information.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ChatUI;
