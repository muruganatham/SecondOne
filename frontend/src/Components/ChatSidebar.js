import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Plus, Search, Home, Trash2, X, Pin, PinOff, Terminal } from 'lucide-react';

function ChatSidebar({
    conversations,
    activeConversationId,
    onSelectConversation,
    onNewChat,
    onDeleteConversation
}) {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isPinned, setIsPinned] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [hoverTimeout, setHoverTimeout] = useState(null);

    // Load pinned state from localStorage
    useEffect(() => {
        const pinned = localStorage.getItem('sidebarPinned') === 'true';
        setIsPinned(pinned);
        setIsExpanded(pinned);
    }, []);

    // Handle mouse enter with delay
    const handleMouseEnter = () => {
        if (!isPinned) {
            const timeout = setTimeout(() => {
                setIsExpanded(true);
            }, 200); // 200ms delay before expanding
            setHoverTimeout(timeout);
        }
    };

    // Handle mouse leave
    const handleMouseLeave = () => {
        if (hoverTimeout) {
            clearTimeout(hoverTimeout);
        }
        if (!isPinned) {
            setIsExpanded(false);
        }
    };

    // Toggle pin state
    const togglePin = () => {
        const newPinned = !isPinned;
        setIsPinned(newPinned);
        setIsExpanded(newPinned);
        localStorage.setItem('sidebarPinned', newPinned.toString());
    };

    // Filter conversations by search
    const filteredConversations = conversations.filter(conv =>
        conv.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Group conversations by date
    const groupConversationsByDate = (convs) => {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        const groups = {
            today: [],
            yesterday: [],
            older: []
        };

        convs.forEach(conv => {
            const convDate = new Date(conv.timestamp);
            const convDateStr = convDate.toDateString();

            if (convDateStr === today.toDateString()) {
                groups.today.push(conv);
            } else if (convDateStr === yesterday.toDateString()) {
                groups.yesterday.push(conv);
            } else {
                groups.older.push(conv);
            }
        });

        return groups;
    };

    const groupedConversations = groupConversationsByDate(filteredConversations);

    return (
        <motion.div
            className={`fixed left-0 top-0 h-screen bg-[#050505]/95 backdrop-blur-xl border-r border-white/5 flex flex-col z-40 overflow-hidden transition-all duration-300 ease-out shadow-2xl shadow-black peer ${isExpanded ? 'expanded w-64' : 'w-16'} ${isPinned ? 'pinned' : ''}`}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            initial={{ width: 64 }}
            animate={{ width: isExpanded ? 256 : 64 }}
            transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
        >
            {/* Navigation Rail Items */}
            <div className="flex flex-col gap-2 p-3 border-b border-white/5 shrink-0">
                <a href="/" className="flex items-center gap-3 p-3 rounded-lg cursor-pointer text-gray-400 transition-all hover:bg-white/5 hover:text-[#00ff9d] group" title="Dashboard">
                    <Home size={20} />
                    {isExpanded && <span className="whitespace-nowrap font-medium text-sm">Dashboard</span>}
                </a>

                <div className="flex items-center gap-3 p-3 rounded-lg cursor-pointer bg-[#00ff9d]/5 text-[#00ff9d] border border-[#00ff9d]/20 group shadow-[0_0_15px_rgba(0,255,157,0.1)]" title="Chats">
                    <Terminal size={20} />
                    {isExpanded && <span className="whitespace-nowrap font-medium text-sm">Active Session</span>}
                </div>

                <button
                    className="flex items-center gap-3 p-3 rounded-lg cursor-pointer bg-[#00ff9d] text-black hover:bg-[#00cc7d] shadow-[0_0_15px_rgba(0,255,157,0.3)] hover:shadow-[0_0_25px_rgba(0,255,157,0.5)] transition-all mt-2"
                    onClick={onNewChat}
                    title="New Chat"
                >
                    <Plus size={20} strokeWidth={2.5} />
                    {isExpanded && <span className="whitespace-nowrap font-bold text-sm">NEW TERMINAL</span>}
                </button>

                <div className="h-[1px] bg-white/5 my-2" />

                {/* Pin/Unpin Button */}
                {isExpanded && (
                    <motion.button
                        className="flex items-center gap-3 p-2 rounded-lg cursor-pointer text-gray-500 hover:text-gray-300 hover:bg-white/5 text-xs uppercase tracking-wider"
                        onClick={togglePin}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        title={isPinned ? "Unpin sidebar" : "Pin sidebar"}
                    >
                        {isPinned ? <PinOff size={14} /> : <Pin size={14} />}
                        <span className="whitespace-nowrap">{isPinned ? 'Unpin Sidebar' : 'Pin Sidebar'}</span>
                    </motion.button>
                )}
            </div>

            {/* Conversations Section (only visible when expanded) */}
            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        className="flex-1 flex flex-col overflow-hidden p-3"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.2 }}
                    >
                        {/* Search Bar */}
                        <div className="flex items-center gap-2 p-2.5 bg-black/40 border border-white/10 rounded-lg mb-4 focus-within:border-[#00ff9d]/50 focus-within:ring-1 focus-within:ring-[#00ff9d]/50 transition-all">
                            <Search size={14} className="text-gray-500" />
                            <input
                                type="text"
                                placeholder="SEARCH LOGS..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="flex-1 bg-transparent border-none outline-none text-xs text-gray-300 placeholder-gray-600 min-w-0 font-mono"
                            />
                            {searchQuery && (
                                <button onClick={() => setSearchQuery('')} className="p-1 text-gray-500 hover:text-white rounded-full hover:bg-white/10">
                                    <X size={12} />
                                </button>
                            )}
                        </div>

                        {/* Conversations List */}
                        <div className="flex-1 overflow-y-auto pr-1 scrollbar-hide">
                            {filteredConversations.length === 0 ? (
                                <div className="flex flex-col items-center justify-center py-10 text-gray-600 text-center">
                                    <MessageSquare size={24} className="opacity-20 mb-2" />
                                    <span className="text-xs font-mono">NO LOGS FOUND</span>
                                </div>
                            ) : (
                                <>
                                    {groupedConversations.today.length > 0 && (
                                        <div className="mb-4">
                                            <div className="text-[10px] font-bold uppercase tracking-widest text-gray-600 px-2 py-2 mb-1">Today</div>
                                            {groupedConversations.today.map(conv => (
                                                <ConversationItem
                                                    key={conv.id}
                                                    conversation={conv}
                                                    isActive={conv.id === activeConversationId}
                                                    onSelect={() => onSelectConversation(conv.id)}
                                                    onDelete={() => onDeleteConversation(conv.id)}
                                                />
                                            ))}
                                        </div>
                                    )}

                                    {groupedConversations.yesterday.length > 0 && (
                                        <div className="mb-4">
                                            <div className="text-[10px] font-bold uppercase tracking-widest text-gray-600 px-2 py-2 mb-1">Yesterday</div>
                                            {groupedConversations.yesterday.map(conv => (
                                                <ConversationItem
                                                    key={conv.id}
                                                    conversation={conv}
                                                    isActive={conv.id === activeConversationId}
                                                    onSelect={() => onSelectConversation(conv.id)}
                                                    onDelete={() => onDeleteConversation(conv.id)}
                                                />
                                            ))}
                                        </div>
                                    )}

                                    {groupedConversations.older.length > 0 && (
                                        <div className="mb-4">
                                            <div className="text-[10px] font-bold uppercase tracking-widest text-gray-600 px-2 py-2 mb-1">Archived</div>
                                            {groupedConversations.older.map(conv => (
                                                <ConversationItem
                                                    key={conv.id}
                                                    conversation={conv}
                                                    isActive={conv.id === activeConversationId}
                                                    onSelect={() => onSelectConversation(conv.id)}
                                                    onDelete={() => onDeleteConversation(conv.id)}
                                                />
                                            ))}
                                        </div>
                                    )}
                                </>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

// Conversation Item Component
function ConversationItem({ conversation, isActive, onSelect, onDelete }) {
    const [showConfirm, setShowConfirm] = useState(false);

    return (
        <motion.div
            className={`flex items-center gap-3 p-2.5 rounded-lg cursor-pointer transition-all mb-1 group relative ${isActive ? 'bg-[#00ff9d]/10 border-l-2 border-[#00ff9d] pl-[8px]' : 'hover:bg-white/5 border-l-2 border-transparent hover:border-gray-700'}`}
            onClick={onSelect}
            whileHover={{ x: 2 }}
        >
            <div className={`w-6 h-6 rounded flex items-center justify-center shrink-0 transition-colors ${isActive ? 'text-[#00ff9d]' : 'text-gray-600 group-hover:text-gray-400'}`}>
                <Terminal size={14} />
            </div>

            <div className="flex-1 min-w-0">
                <div className={`text-xs font-medium truncate font-mono ${isActive ? 'text-[#00ff9d]' : 'text-gray-400'}`}>
                    {conversation.title || 'Untitled Session'}
                </div>
                <div className="text-[10px] text-gray-600 truncate">
                    {conversation.messages ? conversation.messages.length : 0} ops
                </div>
            </div>

            {/* Delete Button / Confirmation */}
            <AnimatePresence>
                {showConfirm ? (
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        className="absolute right-0 top-0 bottom-0 flex items-center gap-1 bg-black pl-2 shadow-lg rounded-r-lg z-10"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            className="p-1.5 bg-red-900/50 text-red-400 rounded hover:bg-red-900 transition-colors"
                            onClick={(e) => {
                                e.stopPropagation();
                                onDelete();
                                setShowConfirm(false);
                            }}
                            title="Confirm"
                        >
                            <Trash2 size={12} />
                        </button>
                        <button
                            className="p-1.5 bg-gray-800 text-gray-400 rounded hover:bg-gray-700 transition-colors"
                            onClick={(e) => {
                                e.stopPropagation();
                                setShowConfirm(false);
                            }}
                            title="Cancel"
                        >
                            <X size={12} />
                        </button>
                    </motion.div>
                ) : (
                    <motion.button
                        className="opacity-0 group-hover:opacity-100 p-1.5 text-gray-600 hover:text-red-400 rounded-md transition-all absolute right-2"
                        onClick={(e) => {
                            e.stopPropagation();
                            setShowConfirm(true);
                        }}
                        title="Delete Log"
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                    >
                        <Trash2 size={14} />
                    </motion.button>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

export default ChatSidebar;
