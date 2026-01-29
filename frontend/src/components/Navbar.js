import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Sun, Moon, Bell, ChevronDown, LogOut } from 'lucide-react';
import { motion } from 'framer-motion';
import '../App.css';

function Navbar() {
    const location = useLocation();

    const [showUserMenu, setShowUserMenu] = React.useState(false);

    // Close dropdown when clicking outside
    React.useEffect(() => {
        const handleClickOutside = (event) => {
            if (!event.target.closest('.profile-section-wrapper')) {
                setShowUserMenu(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/login';
    };

    const [user, setUser] = React.useState({
        name: 'Loading...',
        role: '',
        initials: ''
    });

    React.useEffect(() => {
        const fetchUser = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) return;

                const response = await fetch('http://localhost:8000/api/v1/auth/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    // Get initials from name (e.g., "John Doe" -> "JD")
                    const initials = data.name
                        ? data.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
                        : 'U';

                    setUser({
                        name: data.name || 'User',
                        role: data.role || 'Student',
                        initials: initials
                    });
                }
            } catch (error) {
                console.error('Failed to fetch user profile for navbar', error);
            }
        };

        fetchUser();
    }, []);

    return (
        <motion.nav
            className="navbar"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ type: "spring", stiffness: 100 }}
        >
            <div className="navbar-container">
                {/* Left: Logo */}
                <div className="navbar-logo" onClick={() => setShowUserMenu(!showUserMenu)} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '1.25rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                    <img src="/amypo-logo.jpg" alt="Amypo Logo" className="logo-image" style={{ height: '40px', borderRadius: '8px' }} />
                    Amypo Assistant
                </div>

                {/* Center/Right: Navigation & Actions */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                    {/* Main Nav Links */}
                    <div className="navbar-links" style={{ marginRight: '1rem' }}>
                        <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
                            <LayoutDashboard size={18} />
                            <span>Dashboard</span>
                        </Link>
                        <Link to="/chat" className={`nav-link ${location.pathname === '/chat' ? 'active' : ''}`}>
                            <MessageSquare size={18} />
                            <span>Chat</span>
                        </Link>
                    </div>

                    {/* Right Actions Section */}
                    <div className="navbar-actions">
                        <button className="icon-btn">
                            <Sun size={20} />
                        </button>
                        <button className="icon-btn">
                            <Bell size={20} />
                        </button>

                        {/* User Profile Block */}
                        {/* User Profile Block */}
                        <div className="profile-section-wrapper" style={{ position: 'relative' }}>
                            <div
                                className="profile-section"
                                onClick={() => setShowUserMenu(!showUserMenu)}
                            >
                                <div className="user-avatar-small">
                                    {user.initials}
                                </div>
                                <div className="user-info-mini">
                                    <span className="user-name">{user.name}</span>
                                    <span className="user-role">{user.role}</span>
                                </div>
                                <ChevronDown size={16} color="var(--text-secondary)" />
                            </div>

                            {/* Dropdown Menu */}
                            {showUserMenu && (
                                <motion.div
                                    className="user-dropdown-menu"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: 10 }}
                                >
                                    <div className="dropdown-header">
                                        <div className="user-avatar-small" style={{ width: '32px', height: '32px', fontSize: '0.9rem' }}>
                                            {user.initials}
                                        </div>
                                        <div>
                                            <div className="dropdown-name">{user.name}</div>
                                            <div className="dropdown-email" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{user.role}</div>
                                        </div>
                                    </div>
                                    <div className="dropdown-divider"></div>
                                    <div className="dropdown-divider"></div>
                                    <button className="dropdown-item logout" onClick={handleLogout}>
                                        <LogOut size={16} /> Sign out
                                    </button>
                                </motion.div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </motion.nav>
    );
}

export default Navbar;
