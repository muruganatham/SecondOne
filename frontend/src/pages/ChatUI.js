import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Lightbulb, Download, Terminal, Brain, Cpu, Square, Code, Sparkles } from 'lucide-react';
import ChatSidebar from '../Components/ChatSidebar';
import DataVisualization from '../Components/DataVisualization';
import ConfirmationModal from '../Components/ConfirmationModal';
import { conversationService } from '../services/conversationService';
import logo from '../assets/logo.png'; // Make sure this path is correct
import headerLogo from '../assets/header_logo.png';
import { API_BASE_URL } from '../config';

function ChatUI() {
    // Conversation Management
    const [conversations, setConversations] = useState([]);
    const [activeConversationId, setActiveConversationId] = useState(null);

    // Current Chat State
    const [selectedModel, setSelectedModel] = useState('deepseek-chat');
    const [messages, setMessages] = useState([
        { sender: 'system', text: 'System Initialized. Amypo Access Granted.' }
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
                !(msg.sender === 'ai' && msg.text === 'System Initialized. Amypo Access Granted.' && !msg.sql)
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
            const response = await fetch(`${API_BASE_URL}/ai/ask`, {
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
                setMessages([...updatedMessages, { sender: 'system', text: '🛑 REQUEST TERMINATED.' }]);
                return;
            }
            console.error('Error:', error);
            const errorMessage = {
                sender: 'ai',
                text: 'Error in Data Uplink. Connection Unstable.'
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
            const response = await fetch(`${API_BASE_URL}/ai/ask`, {
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
            { sender: 'system', text: 'System Initialized. Waiting for Query...' }
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
            .map(msg => `${msg.sender === 'user' ? 'USER' : 'SYSTEM'}: ${msg.text}`)
            .join('\n\n');

        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `log-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="flex w-full items-center justify-center h-screen overflow-hidden bg-[#050505] text-[#e0e0e0] font-mono">
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
                <div className="absolute top-0 left-0 right-0 z-10 px-6 py-4 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <Terminal size={20} className="text-[#00ff9d]" />
                        <h1 className="text-xl font-bold text-[#00ff9d] tracking-wider uppercase glitch-effect">
                            AMYPO<span className="text-white">_SYSTEM_V4</span>
                        </h1>
                    </div>
                </div>

                {/* Top Right Controls */}
                <div className="absolute top-4 right-6 z-20 flex items-center gap-3">
                    {/* Model Selector */}
                    <div className="relative group">
                        <button className="flex items-center gap-2 px-3 py-2 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 hover:border-[#00ff9d]/50 transition-all text-sm font-medium text-gray-300 shadow-sm">
                            {selectedModel === 'deepseek-chat' ? (
                                <>
                                    <Code size={16} className="text-[#00ff9d]" />
                                    <span>DEEPSEEK_V2</span>
                                </>
                            ) : (
                                <>
                                    <Cpu size={16} className="text-blue-400" />
                                    <span>OMNI_CORE</span>
                                </>
                            )}
                        </button>

                        {/* Dropdown */}
                        <div className="absolute top-full right-0 mt-2 w-56 bg-[#0a0a0a] rounded-lg shadow-2xl border border-white/10 py-1 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all transform origin-top-right z-50">
                            <button
                                onClick={() => setSelectedModel('deepseek-chat')}
                                className={`w-full text-left px-4 py-3 text-sm flex items-center gap-3 hover:bg-[#00ff9d]/10 transition-colors ${selectedModel === 'deepseek-chat' ? 'text-[#00ff9d]' : 'text-gray-400'}`}
                            >
                                <Code size={16} />
                                <div>
                                    <div className="font-bold tracking-wide">DEEPSEEK_V2</div>
                                    <div className="text-[10px] opacity-70">OPTIMIZED FOR SQL</div>
                                </div>
                            </button>
                            <button
                                onClick={() => setSelectedModel('gpt-4')}
                                className={`w-full text-left px-4 py-3 text-sm flex items-center gap-3 hover:bg-blue-500/10 transition-colors ${selectedModel === 'gpt-4' ? 'text-blue-400' : 'text-gray-400'}`}
                            >
                                <Cpu size={16} />
                                <div>
                                    <div className="font-bold tracking-wide">OMNI_CORE</div>
                                    <div className="text-[10px] opacity-70">REASONING ENGINE</div>
                                </div>
                            </button>
                        </div>
                    </div>

                    {messages.length > 1 && (
                        <motion.button
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            onClick={exportChat}
                            className="px-4 py-2 bg-white/5 backdrop-blur-sm text-[#00ff9d] rounded-lg border border-[#00ff9d]/30 hover:bg-[#00ff9d]/10 transition-all flex items-center gap-2 font-medium text-sm"
                            title="Export Log"
                        >
                            <Download size={16} />
                            <span className="hidden sm:inline">LOGS</span>
                        </motion.button>
                    )}
                </div>

                {/* Messages Area */}
                <div className="flex-1 flex flex-col overflow-hidden pt-16">
                    <div className='flex-1 overflow-hidden flex items-center justify-center w-full'>
                        <div className="w-full max-w-4xl h-full flex flex-col">
                            {messages.length <= 1 ? (
                                <motion.div
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ duration: 0.4 }}
                                    className="flex flex-col items-center justify-center h-full text-center p-8"
                                >
                                    {/* Holographic Logo */}
                                    <motion.div
                                        className="relative mb-8"
                                        initial={{ scale: 0.8, opacity: 0 }}
                                        animate={{ scale: 1, opacity: 1 }}
                                        transition={{ delay: 0.1, duration: 0.5 }}
                                    >
                                        <div className="w-32 h-32 rounded-full flex items-center justify-center border border-[#00ff9d] shadow-[0_0_50px_rgba(0,255,157,0.2)] bg-black relative overflow-hidden">
                                            <div className="absolute inset-0 bg-[url('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGZ4bHk0dGJ6eXJ6Z3B4Z3B4Z3B4Z3B4Z3B4Z3B4Z3B4/Qhe3k1g6w55k4/giphy.gif')] opacity-20 bg-cover mix-blend-overlay"></div>
                                            <Terminal size={48} className="text-[#00ff9d] z-10" />
                                        </div>
                                    </motion.div>

                                    <motion.h1
                                        className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-500 mb-2 tracking-tight"
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.2 }}
                                    >
                                        READY FOR INPUT
                                    </motion.h1>
                                    <motion.p
                                        className="text-sm text-gray-500 max-w-md"
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.3 }}
                                    >
                                        SECURE CONNECTION ESTABLISHED. QUERY THE DATABASE.
                                    </motion.p>
                                </motion.div>
                            ) : (
                                <div ref={messagesContainerRef} className="flex-1 overflow-y-auto py-6 min-h-0 scrollbar-hide pb-32 px-4">
                                    <div className="space-y-6">
                                        <AnimatePresence>
                                            {messages.slice(1).map((msg, index) => (
                                                <motion.div
                                                    key={index}
                                                    className={`flex items-start gap-4 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}
                                                    initial={{ opacity: 0, y: 20 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    transition={{ duration: 0.2 }}
                                                >
                                                    {/* Avatar */}
                                                    <div className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 border ${msg.sender === 'user'
                                                        ? 'bg-purple-900/20 border-purple-500/50 text-purple-400'
                                                        : 'bg-[#00ff9d]/10 border-[#00ff9d]/50 text-[#00ff9d]'
                                                        }`}>
                                                        {msg.sender === 'user' ? <User size={18} /> : <Bot size={18} />}
                                                    </div>

                                                    <div className={`flex-1 min-w-0 max-w-3xl ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
                                                        {/* Message Bubble */}
                                                        <div className={`inline-block p-4 rounded-xl text-[14px] leading-relaxed text-left ${msg.sender === 'user'
                                                            ? 'bg-gradient-to-br from-purple-900/40 to-blue-900/40 border border-purple-500/30 text-gray-100 shadow-[0_0_15px_rgba(168,85,247,0.1)]'
                                                            : 'bg-[#111] border border-white/10 text-gray-300 shadow-lg'
                                                            }`}>
                                                            {msg.text}
                                                        </div>

                                                        {/* SQL Query Block */}
                                                        {msg.sql && !msg.sql.includes("SELECT 'Knowledge Query'") && (
                                                            <motion.div
                                                                className="mt-3 text-left w-full max-w-3xl mx-auto"
                                                                initial={{ opacity: 0, height: 0 }}
                                                                animate={{ opacity: 1, height: 'auto' }}
                                                            >
                                                                <div className="rounded-lg overflow-hidden border border-[#00ff9d]/30 bg-[#050505]/50 backdrop-blur-sm">
                                                                    <div className="bg-[#00ff9d]/10 px-3 py-2 flex items-center gap-2 border-b border-[#00ff9d]/10">
                                                                        <Code size={12} className="text-[#00ff9d]" />
                                                                        <span className="text-[10px] font-bold text-[#00ff9d] uppercase tracking-wider">Generated SQL</span>
                                                                    </div>
                                                                    <pre className="p-3 text-[11px] text-[#00ff9d] font-mono overflow-x-auto">
                                                                        {msg.sql}
                                                                    </pre>
                                                                </div>
                                                            </motion.div>
                                                        )}

                                                        {/* Data Table */}
                                                        {msg.data && Array.isArray(msg.data) && msg.data.length > 0 && (!msg.sql || !msg.sql.includes("SELECT 'Knowledge Query'")) && (
                                                            <motion.div
                                                                className="mt-3 text-left"
                                                                initial={{ opacity: 0 }}
                                                                animate={{ opacity: 1 }}
                                                            >
                                                                <DataVisualization data={msg.data} sql={msg.sql} />
                                                            </motion.div>
                                                        )}

                                                        {/* Follow-up Questions */}
                                                        {msg.sender === 'ai' && index === messages.length - 1 && followUpQuestions.length > 0 && (
                                                            <motion.div
                                                                className="mt-4 flex flex-wrap gap-2 justify-start"
                                                                initial={{ opacity: 0 }}
                                                                animate={{ opacity: 1 }}
                                                                transition={{ delay: 0.3 }}
                                                            >
                                                                {followUpQuestions.map((q, i) => (
                                                                    <button
                                                                        key={i}
                                                                        onClick={() => handleFollowUpClick(q)}
                                                                        className="px-3 py-1.5 rounded-md border border-[#00ff9d]/30 bg-[#00ff9d]/5 text-[#00ff9d] text-xs hover:bg-[#00ff9d]/20 transition-all text-left"
                                                                    >
                                                                        {q}
                                                                    </button>
                                                                ))}
                                                            </motion.div>
                                                        )}
                                                    </div>
                                                </motion.div>
                                            ))}
                                        </AnimatePresence>

                                        {/* Loading State */}
                                        {isLoading && (
                                            <motion.div
                                                className="flex items-start gap-4"
                                                initial={{ opacity: 0 }}
                                                animate={{ opacity: 1 }}
                                            >
                                                <div className="w-9 h-9 rounded-lg flex items-center justify-center bg-[#00ff9d]/10 border border-[#00ff9d]/50">
                                                    <Bot size={18} className="text-[#00ff9d]" />
                                                </div>
                                                <div className="flex items-center gap-1 h-9">
                                                    <span className="w-1.5 h-1.5 bg-[#00ff9d] rounded-full animate-pulse"></span>
                                                    <span className="w-1.5 h-1.5 bg-[#00ff9d] rounded-full animate-pulse delay-75"></span>
                                                    <span className="w-1.5 h-1.5 bg-[#00ff9d] rounded-full animate-pulse delay-150"></span>
                                                </div>
                                            </motion.div>
                                        )}
                                    </div>
                                    <div ref={messagesEndRef} />
                                </div>
                            )}

                            {/* Input Area */}
                            <div className="p-4 relative z-20">
                                <div className="max-w-4xl mx-auto backdrop-blur-2xl bg-[#0a0a0a]/90 border border-white/10 rounded-2xl p-2 flex items-center shadow-2xl shadow-black/50 ring-1 ring-white/5 focus-within:ring-[#00ff9d]/50 focus-within:border-[#00ff9d]/50 transition-all duration-300">
                                    <input
                                        className="flex-1 bg-transparent border-none outline-none text-gray-200 px-4 py-3 placeholder-gray-600 text-sm font-medium"
                                        type="text"
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                                        onFocus={() => {
                                            if (messages.length === 1) {
                                                const aiGreeting = { sender: 'ai', text: 'System Operational. Please input command.' };
                                                setMessages([...messages, aiGreeting]);
                                            }
                                        }}
                                        placeholder="ENTER COMMAND OR QUERY..."
                                        disabled={isLoading}
                                    />
                                    <motion.button
                                        onClick={isLoading ? stopGeneration : sendMessage}
                                        disabled={!isLoading && !input.trim()}
                                        className={`p-3 rounded-xl transition-all flex items-center justify-center ${isLoading
                                            ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30'
                                            : !input.trim()
                                                ? 'bg-white/5 text-gray-600 cursor-not-allowed'
                                                : 'bg-[#00ff9d] text-black hover:bg-[#00cc7d] shadow-[0_0_20px_rgba(0,255,157,0.3)]'
                                            }`}
                                        whileHover={input.trim() ? { scale: 1.05 } : {}}
                                        whileTap={input.trim() ? { scale: 0.95 } : {}}
                                    >
                                        {isLoading ? <Square size={18} fill="currentColor" /> : <Send size={18} strokeWidth={2.5} />}
                                    </motion.button>
                                </div>
                                <div className="text-center mt-3 flex items-center justify-center gap-2 opacity-40">
                                    <span className="w-1.5 h-1.5 rounded-full bg-[#00ff9d]"></span>
                                    <span className="text-[10px] text-gray-400 uppercase tracking-widest">Secure Connection • Codec V4</span>
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
