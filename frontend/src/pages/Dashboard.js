import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Hash, GraduationCap, MessageSquare, Clock, Zap, Search, LayoutDashboard, LogOut, ArrowRight, Terminal } from 'lucide-react';
import PageContainer from '../Components/Layout/PageContainer';
import SuperAdmin from './SuperAdmin';
import { API_BASE_URL } from '../config';

const StatCard = ({ icon: Icon, label, value, trend, color, onClick }) => (
    <motion.div
        whileHover={{ y: -4, boxShadow: "0 10px 30px -10px rgba(0, 255, 157, 0.1)" }}
        className="bg-[#0a0a0a]/80 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-white/5 hover:border-[#00ff9d]/30 transition-all cursor-pointer group relative overflow-hidden"
        onClick={onClick}
    >
        <div className={`absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity text-white`}>
            <Icon size={120} />
        </div>
        <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-xl bg-white/5 text-[#00ff9d] border border-[#00ff9d]/20 shadow-inner group-hover:text-white group-hover:bg-[#00ff9d] transition-all duration-300`}>
                <Icon size={24} />
            </div>
            {trend && (
                <span className="bg-[#00ff9d]/10 text-[#00ff9d] text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1 border border-[#00ff9d]/20 font-mono">
                    {trend}
                </span>
            )}
        </div>
        <div>
            <p className="text-gray-500 text-xs font-mono font-medium mb-1 uppercase tracking-wider">{label}</p>
            <h3 className="text-3xl font-bold text-white tracking-tight">{value}</h3>
        </div>
    </motion.div>
);

const ActionCard = ({ icon: Icon, title, description, onClick, delay }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay }}
        onClick={onClick}
        className="bg-[#0a0a0a]/80 p-6 rounded-2xl border border-white/5 shadow-sm hover:shadow-[0_0_20px_rgba(0,255,157,0.1)] hover:border-[#00ff9d]/40 transition-all cursor-pointer group flex items-start gap-5"
    >
        <div className="p-4 rounded-xl bg-white/5 text-gray-400 group-hover:bg-[#00ff9d] group-hover:text-black transition-all duration-300 shrink-0">
            <Icon size={24} />
        </div>
        <div>
            <h3 className="text-lg font-bold text-gray-200 group-hover:text-[#00ff9d] transition-colors flex items-center gap-2">
                {title}
                <ArrowRight size={16} className="opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300 transform text-[#00ff9d]" />
            </h3>
            <p className="text-gray-500 text-sm leading-relaxed mt-1 group-hover:text-gray-400 font-mono">
                {description}
            </p>
        </div>
    </motion.div>
);

function Dashboard() {
    const navigate = useNavigate();
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
                const response = await fetch(`${API_BASE_URL}/auth/me`, {
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

    const handleNewChat = () => {
        navigate('/chat');
        // Trigger new chat creation
        localStorage.setItem('createNewChat', 'true');
    };

    const handleSearchHistory = () => {
        navigate('/chat');
        // Focus on search after navigation
        setTimeout(() => {
            const searchInput = document.querySelector('.search-input');
            if (searchInput) searchInput.focus();
        }, 100);
    };



    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen bg-[#050505]">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#00ff9d]"></div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="text-center mt-20 p-8 bg-[#0a0a0a] rounded-2xl shadow-2xl max-w-md mx-auto border border-white/10">
                <Terminal size={48} className="text-[#00ff9d] mx-auto mb-4 opacity-50" />
                <p className="text-gray-400 font-medium font-mono mb-6">Unauthorized Access. Please authenticate.</p>
                <button
                    onClick={() => navigate('/login')}
                    className="mt-4 px-6 py-2 bg-[#00ff9d] text-black rounded-xl hover:bg-[#00cc7d] transition-colors font-bold shadow-[0_0_15px_rgba(0,255,157,0.3)]"
                >
                    INITIATE LOGIN
                </button>
            </div>
        );

    }

    // Role-based Dashboard Switching
    if (user.role === 'Super Admin') {
        return <SuperAdmin />;
    }

    return (
        <PageContainer className="py-8 bg-[#050505] min-h-screen text-gray-200">
            {/* Header / Hero Section */}
            <header className="mb-10 text-center sm:text-left">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="max-w-4xl"
                >
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#00ff9d]/10 border border-[#00ff9d]/20 text-[#00ff9d] text-xs font-mono mb-4">
                        <div className="w-2 h-2 rounded-full bg-[#00ff9d] animate-pulse"></div>
                        SYSTEM OPERATIONAL
                    </div>
                    <h1 className="text-4xl font-extrabold text-white tracking-tight mb-3">
                        Welcome Back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#00ff9d] to-emerald-600">{user.name.split(' ')[0]}</span>
                    </h1>
                    <p className="text-lg text-gray-500 font-medium leading-relaxed font-mono max-w-2xl">
                        Neural interface connected. Accessing student database and learning analytics modules.
                    </p>
                </motion.div>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                <StatCard
                    icon={MessageSquare}
                    label="Total Queries"
                    value={user.stats_chat_count || 0}
                    trend="+12%"
                    color="bg-emerald-500"
                    onClick={() => navigate('/chat')}
                />
                <StatCard
                    icon={Zap}
                    label="Tokens Processed"
                    value={user.stats_words_generated ? (user.stats_words_generated > 1000 ? (user.stats_words_generated / 1000).toFixed(1) + 'k' : user.stats_words_generated) : '0'}
                    trend="OPTIMIZED"
                    color="bg-blue-500"
                    onClick={() => { }}
                />
                <StatCard
                    icon={Clock}
                    label="Active Streak"
                    value={`${user.active_streak || 0} Days`}
                    trend="KEEP GOING"
                    color="bg-amber-500"
                    onClick={() => { }}
                />
                <StatCard
                    icon={GraduationCap}
                    label="Clearance Level"
                    value={user.role || 'Student'}
                    trend="ACTIVE"
                    color="bg-purple-500"
                    onClick={() => { }}
                />
            </div>

            {/* Quick Actions & Profile Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Available Actions - Spans 2 columns */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between border-b border-white/5 pb-4">
                        <h2 className="text-xl font-bold text-white flex items-center gap-2">
                            <Terminal size={20} className="text-[#00ff9d]" />
                            Command Modules
                        </h2>
                        <button
                            onClick={handleNewChat}
                            className="text-[#00ff9d] font-bold hover:text-white flex items-center gap-2 text-sm bg-[#00ff9d]/10 border border-[#00ff9d]/30 px-4 py-2 rounded-lg transition-all group hover:bg-[#00ff9d]/20 hover:shadow-[0_0_15px_rgba(0,255,157,0.2)]"
                        >
                            INIT_QUERY <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <ActionCard
                            icon={Search}
                            title="Query Records"
                            description="Deep search student records using natural language processing."
                            onClick={handleNewChat}
                            delay={0.1}
                        />
                        <ActionCard
                            icon={LayoutDashboard}
                            title="Generate Reports"
                            description="Compile visual performance metrics and analytics instantly."
                            onClick={handleNewChat}
                            delay={0.2}
                        />
                        <ActionCard
                            icon={MessageSquare}
                            title="Analyze Feedback"
                            description="Process unstructured student survey data and forms."
                            onClick={handleNewChat}
                            delay={0.3}
                        />
                        <ActionCard
                            icon={Hash}
                            title="Query Logs"
                            description="Audit past search queries and system interaction logs."
                            onClick={handleSearchHistory}
                            delay={0.4}
                        />
                    </div>
                </div>

                {/* Profile Sidebar - Spans 1 column */}
                <div className="lg:col-span-1">
                    <motion.div
                        className="bg-[#0a0a0a]/90 backdrop-blur-xl border border-white/10 rounded-3xl p-8 text-center sticky top-24 shadow-2xl relative overflow-hidden group"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.5 }}
                    >
                        {/* Holographic BG Effect */}
                        <div className="absolute inset-0 bg-gradient-to-br from-[#00ff9d]/5 to-purple-900/10 opacity-50 group-hover:opacity-100 transition-opacity duration-700"></div>

                        <div className="relative inline-block mb-6 group/avatar z-10">
                            <div className="absolute -inset-2 bg-gradient-to-tr from-[#00ff9d] to-emerald-600 rounded-full opacity-20 group-hover/avatar:opacity-40 blur-md transition duration-500 animate-pulse"></div>
                            <img
                                src={`https://ui-avatars.com/api/?name=${user.name.replace(' ', '+')}&background=000&color=00ff9d&size=128&bold=true`}
                                alt="Profile"
                                className="relative w-28 h-28 rounded-full border-2 border-[#00ff9d]/50 shadow-[0_0_20px_rgba(0,255,157,0.2)] mx-auto p-1 bg-black"
                            />
                            <div className="absolute bottom-1 right-2 w-4 h-4 bg-[#00ff9d] border-2 border-black rounded-full shadow-[0_0_10px_#00ff9d]"></div>
                        </div>

                        <h3 className="text-xl font-bold text-white mb-1 tracking-wide z-10 relative">{user.name}</h3>
                        <p className="text-gray-500 text-xs font-mono mb-6 uppercase tracking-widest z-10 relative">{user.role === 'admin' ? 'sys_admin_root' : 'standard_user'}</p>

                        <div className="grid grid-cols-2 gap-4 mb-8 text-sm z-10 relative">
                            <div className="bg-black/50 p-3 rounded-xl border border-white/5 backdrop-blur-sm">
                                <span className="block text-gray-500 text-[10px] uppercase font-bold mb-1">ID / Email</span>
                                <span className="font-mono text-gray-300 truncate text-xs" title={user.email}>{user.email.split('@')[0]}</span>
                            </div>
                            <div className="bg-black/50 p-3 rounded-xl border border-white/5 backdrop-blur-sm">
                                <span className="block text-gray-500 text-[10px] uppercase font-bold mb-1">Affiliation</span>
                                <span className="font-mono text-gray-300 truncate text-xs" title={user.college}>{user.college || 'N/A'}</span>
                            </div>
                        </div>

                        <button
                            className="w-full flex items-center justify-center gap-2 text-gray-400 hover:text-red-400 hover:bg-red-900/10 py-3 rounded-xl transition-all font-bold border border-white/5 hover:border-red-500/30 group z-10 relative text-sm uppercase tracking-wide"
                            onClick={() => {
                                localStorage.removeItem('token');
                                window.location.href = '/login';
                            }}
                        >
                            <LogOut size={16} className="group-hover:translate-x-1 transition-transform" />
                            <span>Terminate Session</span>
                        </button>
                    </motion.div>
                </div>
            </div>
        </PageContainer>
    );
}

export default Dashboard;
