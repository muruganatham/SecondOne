import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Plus, Search, Home, Trash2, X, Pin, PinOff } from 'lucide-react';

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
            className={`fixed left-0 top-0 h-screen bg-white/90 backdrop-blur-md border-r border-slate-200 flex flex-col z-40 overflow-hidden transition-all duration-300 ease-out shadow-sm peer ${isExpanded ? 'expanded w-56 shadow-xl' : 'w-16'} ${isPinned ? 'pinned' : ''}`}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            initial={{ width: 64 }}
            animate={{ width: isExpanded ? 224 : 64 }}
            transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
        >
            {/* Navigation Rail Items */}
            <div className="flex flex-col gap-1 p-2 border-b border-slate-200 shrink-0">
                <a href="/" className="flex items-center gap-3 p-3 rounded-xl cursor-pointer text-slate-500 transition-all hover:bg-slate-100 hover:text-slate-900 group" title="Dashboard">
                    <Home size={20} />
                    {isExpanded && <span className="whitespace-nowrap font-medium">Dashboard</span>}
                </a>

                <div className="flex items-center gap-3 p-3 rounded-xl cursor-pointer bg-primary/10 text-primary font-medium group" title="Chats">
                    <MessageSquare size={20} />
                    {isExpanded && <span className="whitespace-nowrap">Chats</span>}
                </div>

                <button className="flex items-center gap-3 p-3 rounded-xl cursor-pointer bg-primary text-white hover:bg-primary-hover shadow-md hover:shadow-lg transition-all" onClick={onNewChat} title="New Chat">
                    <Plus size={20} />
                    {isExpanded && <span className="whitespace-nowrap font-medium">New Chat</span>}
                </button>

                <div className="h-[1px] bg-slate-200 my-2" />

                {/* Pin/Unpin Button */}
                {isExpanded && (
                    <motion.button
                        className="flex items-center gap-3 p-3 rounded-xl cursor-pointer text-slate-400 hover:text-slate-600 hover:bg-slate-50 text-sm"
                        onClick={togglePin}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        title={isPinned ? "Unpin sidebar" : "Pin sidebar"}
                    >
                        {isPinned ? <PinOff size={18} /> : <Pin size={18} />}
                        <span className="whitespace-nowrap">{isPinned ? 'Unpin' : 'Pin'}</span>
                    </motion.button>
                )}

                {/*                
                <button
                    className="flex items-center gap-3 p-3 rounded-xl cursor-pointer text-slate-500 transition-all hover:bg-red-50 hover:text-red-600 group"
                    onClick={() => {
                        localStorage.removeItem('token');
                        window.location.href = '/login';
                    }}
                    title="Sign Out"
                >
                    <LogOut size={20} />
                    {isExpanded && <span className="whitespace-nowrap font-medium">Sign Out</span>}
                </button> */}
            </div>

            {/* Conversations Section (only visible when expanded) */}
            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        className="flex-1 flex flex-col overflow-hidden p-2"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.2 }}
                    >
                        {/* Search Bar */}
                        <div className="flex items-center gap-2 p-2.5 bg-slate-100 border border-slate-200 rounded-xl mb-3 focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/10 transition-all">
                            <Search size={16} className="text-slate-400" />
                            <input
                                type="text"
                                placeholder="Search chats..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="flex-1 bg-transparent border-none outline-none text-sm text-slate-800 placeholder-slate-400 min-w-0"
                            />
                            {searchQuery && (
                                <button onClick={() => setSearchQuery('')} className="p-1 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-200">
                                    <X size={14} />
                                </button>
                            )}
                        </div>

                        {/* Conversations List */}
                        <div className="flex-1 overflow-y-auto pr-1">
                            {filteredConversations.length === 0 ? (
                                <div className="flex flex-col items-center justify-center py-10 text-slate-400 text-center">
                                    <MessageSquare size={32} className="opacity-50 mb-3" />
                                    <p className="text-sm font-semibold text-slate-500">No conversations yet</p>
                                    <span className="text-xs">Start a new chat to begin</span>
                                </div>
                            ) : (
                                <>
                                    {groupedConversations.today.length > 0 && (
                                        <div className="mb-4">
                                            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 py-2">Today</div>
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
                                            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 py-2">Yesterday</div>
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
                                            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 py-2">Older</div>
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
// Conversation Item Component
function ConversationItem({ conversation, isActive, onSelect, onDelete }) {
    const [showConfirm, setShowConfirm] = useState(false);

    return (
        <motion.div
            className={`flex items-center gap-3 p-2.5 rounded-lg cursor-pointer transition-colors mb-0.5 group relative ${isActive ? 'bg-primary/10 border-l-2 border-primary pl-[8px]' : 'hover:bg-slate-100 border-l-2 border-transparent'}`}
            onClick={onSelect}
            whileHover={{ x: 2 }}
        >
            <div className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 transition-colors ${isActive ? 'bg-primary text-white' : 'bg-slate-200 text-slate-500 group-hover:bg-white'}`}>
                <MessageSquare size={16} />
            </div>

            <div className="flex-1 min-w-0">
                <div className={`text-sm font-medium truncate ${isActive ? 'text-primary' : 'text-slate-700'}`}>
                    {conversation.title || 'Untitled Chat'}
                </div>
                <div className="text-xs text-slate-400">
                    {conversation.messages ? conversation.messages.length : 0} messages
                </div>
            </div>

            {/* Delete Button / Confirmation */}
            <AnimatePresence>
                {showConfirm ? (
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        className="absolute right-0 top-0 bottom-0 flex items-center gap-1 bg-white/95 backdrop-blur-sm pl-2 shadow-sm rounded-r-lg"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <span className="text-[10px] font-semibold text-slate-500 mr-1">Delete?</span>
                        <button
                            className="p-1.5 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
                            onClick={(e) => {
                                e.stopPropagation();
                                onDelete();
                                setShowConfirm(false);
                            }}
                            title="Confirm Delete"
                        >
                            <Trash2 size={14} />
                        </button>
                        <button
                            className="p-1.5 bg-slate-200 text-slate-600 rounded-md hover:bg-slate-300 transition-colors"
                            onClick={(e) => {
                                e.stopPropagation();
                                setShowConfirm(false);
                            }}
                            title="Cancel"
                        >
                            <X size={14} />
                        </button>
                    </motion.div>
                ) : (
                    <motion.button
                        className="opacity-0 group-hover:opacity-100 p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-md transition-all absolute right-2"
                        onClick={(e) => {
                            e.stopPropagation();
                            setShowConfirm(true);
                        }}
                        title="Delete conversation"
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                    >
                        <Trash2 size={16} />
                    </motion.button>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

export default ChatSidebar;
