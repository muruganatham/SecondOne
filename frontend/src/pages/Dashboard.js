import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Hash, BookOpen, Briefcase, GraduationCap, MessageSquare, Clock, Zap, Plus, Search } from 'lucide-react';
import '../App.css';

function Dashboard() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    // Handle unauthenticated state if needed
                    setLoading(false);
                    return;
                }
                const response = await fetch('http://localhost:8000/api/v1/auth/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    setUser(data);
                }
            } catch (error) {
                console.error('Error fetching profile:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchUserProfile();
    }, []);

    if (loading) {
        return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'var(--text-primary)' }}>Loading...</div>;
    }

    if (!user) {
        return <div style={{ textAlign: 'center', marginTop: '50px' }}>Please log in to view dashboard.</div>;
    }

    return (
        <div className="dashboard-container">
            <motion.div
                className="welcome-section"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h1>Welcome back, {user.name.split(' ')[0]}!</h1>
                <p>Here's what's happening with your academic profile today.</p>
            </motion.div>

            <div className="dashboard-grid">
                {/* Left Main Column */}
                <div className="main-content">
                    {/* Stats Row */}
                    <div className="stats-grid">
                        <motion.div className="stat-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
                            <div className="stat-icon-wrapper" style={{ background: 'rgba(46, 139, 87, 0.1)', color: '#2E8B57' }}>
                                <MessageSquare size={24} />
                            </div>
                            <div className="stat-info">
                                <h3>Total Chats</h3>
                                <p>{user.stats_chat_count || 0}</p>
                            </div>
                        </motion.div>
                        <motion.div className="stat-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                            <div className="stat-icon-wrapper" style={{ background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' }}>
                                <Zap size={24} />
                            </div>
                            <div className="stat-info">
                                <h3>Words Generated</h3>
                                <p>{user.stats_words_generated ? (user.stats_words_generated > 1000 ? (user.stats_words_generated / 1000).toFixed(1) + 'k' : user.stats_words_generated) : '0'}</p>
                            </div>
                        </motion.div>
                        <motion.div className="stat-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
                            <div className="stat-icon-wrapper" style={{ background: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>
                                <Clock size={24} />
                            </div>
                            <div className="stat-info">
                                <h3>Active Streak</h3>
                                <p>{user.active_streak || 0} Days</p>
                            </div>
                        </motion.div>
                    </div>

                    {/* Quick Actions */}
                    <div className="section-header">
                        <h2>Quick Actions</h2>
                    </div>
                    <div className="quick-actions-grid">
                        <motion.div className="action-card" whileHover={{ scale: 1.02 }}>
                            <Plus size={24} style={{ color: 'var(--primary-color)' }} />
                            <div>
                                <h4 style={{ margin: 0, color: 'var(--text-primary)' }}>New Chat</h4>
                                <p style={{ margin: '4px 0 0', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Start a new conversation</p>
                            </div>
                        </motion.div>
                        <motion.div className="action-card" whileHover={{ scale: 1.02 }}>
                            <Search size={24} style={{ color: 'var(--primary-color)' }} />
                            <div>
                                <h4 style={{ margin: 0, color: 'var(--text-primary)' }}>Search History</h4>
                                <p style={{ margin: '4px 0 0', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Find past topics</p>
                            </div>
                        </motion.div>
                    </div>

                    {/* Activity Feed */}
                    <div className="section-header" style={{ marginTop: '32px' }}>
                        <h2>Recent Activity</h2>
                    </div>
                    <div className="activity-feed">
                        <div className="activity-item">
                            <div className="activity-icon"><MessageSquare size={18} /></div>
                            <div className="activity-content">
                                <h4>React Hooks query</h4>
                                <p>Asked about useEffect dependency array</p>
                            </div>
                            <span className="activity-time">2h ago</span>
                        </div>
                        <div className="activity-item">
                            <div className="activity-icon"><BookOpen size={18} /></div>
                            <div className="activity-content">
                                <h4>Python Scripting</h4>
                                <p>Generated a file parsing script</p>
                            </div>
                            <span className="activity-time">5h ago</span>
                        </div>
                        <div className="activity-item">
                            <div className="activity-icon"><Zap size={18} /></div>
                            <div className="activity-content">
                                <h4>System Update</h4>
                                <p>Profile details updated successfully</p>
                            </div>
                            <span className="activity-time">1d ago</span>
                        </div>
                    </div>
                </div>

                {/* Right Sidebar - Profile */}
                <div className="sidebar">
                    <motion.div
                        className="profile-sidebar-card"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.4 }}
                    >
                        <div className="profile-avatar-large">
                            {user.name.charAt(0)}
                        </div>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '4px', color: 'var(--text-primary)' }}>{user.name}</h2>
                        <span style={{
                            background: 'rgba(46, 139, 87, 0.1)',
                            color: '#2E8B57',
                            padding: '4px 12px',
                            borderRadius: '20px',
                            fontSize: '0.9rem',
                            fontWeight: '600'
                        }}>{user.role}</span>

                        <div style={{ marginTop: '32px', textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-secondary)' }}>
                                <Mail size={18} />
                                <span style={{ fontSize: '0.95rem' }}>{user.email}</span>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-secondary)' }}>
                                <Hash size={18} />
                                <span style={{ fontSize: '0.95rem' }}>{user.roll_no || 'N/A'}</span>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-secondary)' }}>
                                <BookOpen size={18} />
                                <span style={{ fontSize: '0.95rem' }}>{user.department || 'N/A'}</span>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-secondary)' }}>
                                <GraduationCap size={18} />
                                <span style={{ fontSize: '0.95rem' }}>{user.college || 'N/A'}</span>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
