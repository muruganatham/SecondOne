import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Sun, Bell, ChevronDown, LogOut, Terminal, User, Trophy } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { API_BASE_URL } from '../config';

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

                const response = await fetch(`${API_BASE_URL}/auth/me`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    const initials = data.name
                        ? data.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
                        : 'OP';

                    setUser({
                        name: data.name || 'Operator',
                        role: data.role || 'User',
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
            className="sticky top-0 z-50 h-16 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5 shadow-2xl"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ type: "spring", stiffness: 100 }}
        >
            <div className="w-full h-full flex items-center justify-between px-6 gap-4 max-w-7xl mx-auto">
                {/* Left: Logo */}
                <Link
                    to="/"
                    className="flex items-center gap-3 group"
                >
                    <div className="w-10 h-10 rounded-lg bg-[#00ff9d]/10 border border-[#00ff9d]/20 flex items-center justify-center text-[#00ff9d] shadow-[0_0_10px_rgba(0,255,157,0.1)] group-hover:shadow-[0_0_20px_rgba(0,255,157,0.3)] transition-all">
                        <Terminal size={20} strokeWidth={2.5} />
                    </div>
                    <div className="flex flex-col">
                        <span className="text-lg font-bold text-white tracking-wider font-mono group-hover:text-[#00ff9d] transition-colors">AMYPO<span className="opacity-50 text-xs ml-1 align-top">V4</span></span>
                        <span className="text-[10px] text-gray-500 uppercase tracking-widest leading-none">Intelligent System</span>
                    </div>
                </Link>

                {/* Center/Right: Navigation & Actions */}
                <div className="flex items-center gap-8">
                    {/* Main Nav Links */}
                    <div className="flex items-center gap-1 mr-4">
                        <Link to="/" className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${location.pathname === '/' ? 'text-[#00ff9d] bg-[#00ff9d]/10' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}>
                            <LayoutDashboard size={16} />
                            <span className="font-mono">DASHBOARD</span>
                        </Link>
                        <Link to="/chat" className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${location.pathname === '/chat' ? 'text-[#00ff9d] bg-[#00ff9d]/10' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}>
                            <MessageSquare size={16} />
                            <span className="font-mono">TERMINAL</span>
                        </Link>
                        <Link to="/leaderboard" className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${location.pathname === '/leaderboard' ? 'text-[#00ff9d] bg-[#00ff9d]/10' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}>
                            <Trophy size={16} />
                            <span className="font-mono">LEADERBOARD</span>
                        </Link>
                    </div>

                    {/* Right Actions Section */}
                    <div className="flex items-center gap-4 pl-4 border-l border-white/10">
                        <button className="relative p-2 rounded-lg text-gray-500 hover:text-[#00ff9d] hover:bg-[#00ff9d]/10 transition-colors flex items-center justify-center">
                            <Bell size={18} />
                            <span className="absolute top-2 right-2 w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse border border-black"></span>
                        </button>

                        {/* User Profile Block */}
                        <div className="relative profile-section-wrapper">
                            <div
                                className="flex items-center gap-3 pl-2 cursor-pointer group"
                                onClick={() => setShowUserMenu(!showUserMenu)}
                            >
                                <div className="text-right hidden sm:block">
                                    <div className="text-xs font-bold text-gray-200 font-mono group-hover:text-[#00ff9d] transition-colors">{user.name}</div>
                                    <div className="text-[10px] text-gray-500 uppercase tracking-wider">{user.role}</div>
                                </div>
                                <div className="w-9 h-9 bg-black border border-white/10 rounded-lg flex items-center justify-center text-xs font-bold text-[#00ff9d] shadow-sm group-hover:border-[#00ff9d]/50 transition-all overflow-hidden relative">
                                    <div className="absolute inset-0 bg-[#00ff9d]/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                    {user.initials}
                                </div>
                            </div>

                            {/* Dropdown Menu */}
                            <AnimatePresence>
                                {showUserMenu && (
                                    <motion.div
                                        className="absolute right-0 top-full mt-4 w-60 bg-[#0a0a0a] rounded-xl shadow-2xl border border-white/10 py-1 z-50 overflow-hidden"
                                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                                        animate={{ opacity: 1, y: 0, scale: 1 }}
                                        exit={{ opacity: 0, y: 10, scale: 0.95 }}
                                        transition={{ duration: 0.1 }}
                                    >
                                        <div className="px-4 py-3 border-b border-white/5 bg-white/5">
                                            <div className="flex items-center gap-3">
                                                <div className="w-8 h-8 bg-[#00ff9d]/20 text-[#00ff9d] rounded-lg flex items-center justify-center text-xs font-bold border border-[#00ff9d]/30">
                                                    {user.initials}
                                                </div>
                                                <div className="overflow-hidden">
                                                    <div className="font-bold text-gray-200 text-sm truncate">{user.name}</div>
                                                    <div className="text-[10px] text-gray-500 font-mono uppercase tracking-wider">{user.role}</div>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="p-1">
                                            <button className="w-full px-3 py-2 text-left text-xs font-medium text-gray-400 hover:text-white hover:bg-white/5 rounded-lg flex items-center gap-2 transition-colors">
                                                <User size={14} /> ACCOUNT SETTINGS
                                            </button>
                                            <div className="h-px bg-white/5 my-1" />
                                            <button
                                                className="w-full px-3 py-2 text-left text-xs font-medium text-red-400 hover:bg-red-500/10 hover:text-red-300 rounded-lg flex items-center gap-2 transition-colors"
                                                onClick={handleLogout}
                                            >
                                                <LogOut size={14} /> TERMINATE SESSION
                                            </button>
                                        </div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    </div>
                </div>
            </div>
        </motion.nav>
    );
}

export default Navbar;
