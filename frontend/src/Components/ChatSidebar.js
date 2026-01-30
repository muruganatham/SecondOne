import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Plus, MessageSquare, Trash2, X } from 'lucide-react';
import '../App.css';

function ChatSidebar({
    conversations,
    activeConversationId,
    onSelectConversation,
    onNewChat,
    onDeleteConversation,
    isOpen,
    onToggle
}) {
    const [searchQuery, setSearchQuery] = useState('');

    const filteredConversations = conversations.filter(conv =>
        conv.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Group conversations by date
    const groupedConversations = filteredConversations.reduce((groups, conv) => {
        const date = new Date(conv.timestamp);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        let label;
        if (date.toDateString() === today.toDateString()) {
            label = 'Today';
        } else if (date.toDateString() === yesterday.toDateString()) {
            label = 'Yesterday';
        } else {
            label = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }

        if (!groups[label]) groups[label] = [];
        groups[label].push(conv);
        return groups;
    }, {});

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    className="chat-sidebar"
                    initial={{ x: -300, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    exit={{ x: -300, opacity: 0 }}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                >
                    {/* Header */}
                    <div className="sidebar-header">
                        <button className="new-chat-btn" onClick={onNewChat}>
                            <Plus size={18} />
                            <span>New Chat</span>
                        </button>
                        <button className="sidebar-close-btn" onClick={onToggle}>
                            <X size={20} />
                        </button>
                    </div>

                    {/* Search */}
                    <div className="sidebar-search">
                        <Search size={16} />
                        <input
                            type="text"
                            placeholder="Search conversations..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>

                    {/* Conversation List */}
                    <div className="sidebar-conversations">
                        {Object.entries(groupedConversations).map(([label, convs]) => (
                            <div key={label} className="conversation-group">
                                <div className="group-label">{label}</div>
                                {convs.map(conv => (
                                    <motion.div
                                        key={conv.id}
                                        className={`conversation-item ${activeConversationId === conv.id ? 'active' : ''}`}
                                        onClick={() => onSelectConversation(conv.id)}
                                        whileHover={{ x: 4 }}
                                        transition={{ type: 'spring', stiffness: 400 }}
                                    >
                                        <div className="conversation-icon">
                                            <MessageSquare size={16} />
                                        </div>
                                        <div className="conversation-content">
                                            <div className="conversation-title">{conv.title}</div>
                                            <div className="conversation-meta">
                                                {conv.messageCount} messages
                                            </div>
                                        </div>
                                        <button
                                            className="conversation-delete"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                onDeleteConversation(conv.id);
                                            }}
                                        >
                                            <Trash2 size={14} />
                                        </button>
                                    </motion.div>
                                ))}
                            </div>
                        ))}

                        {filteredConversations.length === 0 && (
                            <div className="empty-state">
                                <MessageSquare size={40} color="var(--text-light)" />
                                <p>No conversations yet</p>
                                <span>Start a new chat to begin</span>
                            </div>
                        )}
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}

export default ChatSidebar;
