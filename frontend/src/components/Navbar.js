import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Sun, Bell, ChevronDown, LogOut } from 'lucide-react';
import { motion } from 'framer-motion';


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
            className="sticky top-0 z-50 h-16 bg-slate-50 border-b border-slate-200 shadow-sm"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ type: "spring", stiffness: 100 }}
        >
            <div className="w-full h-full flex items-center justify-between px-0 gap-4">
                {/* Left: Logo */}
                <div
                    className="flex items-center gap-3 text-xl font-bold text-slate-800 cursor-pointer"
                    onClick={() => setShowUserMenu(!showUserMenu)}
                >
                    <img src="/logo.png" alt="Amypo Logo" className="h-12 w-auto" />
                    <span className="text-slate-800">Amypo Assistant</span>
                </div>

                {/* Center/Right: Navigation & Actions */}
                <div className="flex items-center gap-8">
                    {/* Main Nav Links */}
                    <div className="flex items-center gap-8 mr-4">
                        <Link to="/" className={`relative py-5 text-[15px] font-medium transition-colors hover:text-primary flex items-center gap-2 ${location.pathname === '/' ? 'text-primary' : 'text-slate-500'}`}>
                            <LayoutDashboard size={18} />
                            <span>Dashboard</span>
                            {location.pathname === '/' && (
                                <span className="absolute bottom-0 left-0 w-full h-[2px] bg-primary" />
                            )}
                        </Link>
                        <Link to="/chat" className={`relative py-5 text-[15px] font-medium transition-colors hover:text-primary flex items-center gap-2 ${location.pathname === '/chat' ? 'text-primary' : 'text-slate-500'}`}>
                            <MessageSquare size={18} />
                            <span>Chat</span>
                            {location.pathname === '/chat' && (
                                <span className="absolute bottom-0 left-0 w-full h-[2px] bg-primary" />
                            )}
                        </Link>
                    </div>

                    {/* Right Actions Section */}
                    <div className="flex items-center gap-6">
                        <button className="p-2 rounded-full text-slate-500 hover:text-primary hover:bg-slate-100 transition-colors flex items-center justify-center">
                            <Sun size={20} />
                        </button>
                        <button className="p-2 rounded-full text-slate-500 hover:text-primary hover:bg-slate-100 transition-colors flex items-center justify-center">
                            <Bell size={20} />
                        </button>

                        {/* User Profile Block */}
                        <div className="relative profile-section-wrapper">
                            <div
                                className="flex items-center gap-3 pl-6 border-l border-slate-200 cursor-pointer hover:opacity-80 transition-opacity"
                                onClick={() => setShowUserMenu(!showUserMenu)}
                            >
                                <div className="w-10 h-10 bg-emerald-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                                    {user.initials}
                                </div>
                                <div className="flex flex-col items-start">
                                    <span className="text-sm font-semibold text-slate-800 leading-tight">{user.name}</span>
                                    <span className="text-xs text-slate-500 leading-tight">{user.role}</span>
                                </div>
                                <ChevronDown size={16} className="text-slate-500" />
                            </div>

                            {/* Dropdown Menu */}
                            {showUserMenu && (
                                <motion.div
                                    className="absolute right-0 top-full mt-2 w-64 bg-white rounded-xl shadow-xl border border-slate-100 py-2 z-50"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: 10 }}
                                >
                                    <div className="px-4 py-3 flex items-center gap-3 border-b border-slate-100">
                                        <div className="w-8 h-8 bg-emerald-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                                            {user.initials}
                                        </div>
                                        <div>
                                            <div className="font-semibold text-slate-800">{user.name}</div>
                                            <div className="text-xs text-slate-500">{user.role}</div>
                                        </div>
                                    </div>
                                    <div className="py-2">
                                        <button
                                            className="w-full px-4 py-2 text-left text-sm text-red-500 hover:bg-red-50 flex items-center gap-2 transition-colors"
                                            onClick={handleLogout}
                                        >
                                            <LogOut size={16} /> Sign out
                                        </button>
                                    </div>
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
