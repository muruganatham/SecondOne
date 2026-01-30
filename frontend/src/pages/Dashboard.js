import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Hash, GraduationCap, MessageSquare, Clock, Zap, Search, LayoutDashboard, LogOut, ArrowRight } from 'lucide-react';
import { conversationService } from '../services/conversationService';
import PageContainer from '../components/Layout/PageContainer';


const StatCard = ({ icon: Icon, label, value, trend, color, onClick }) => (
    <motion.div
        whileHover={{ y: -4 }}
        className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-lg transition-all cursor-pointer group relative overflow-hidden"
        onClick={onClick}
    >
        <div className={`absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity ${color.replace('bg-', 'text-')}`}>
            <Icon size={80} />
        </div>
        <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-xl ${color} text-white shadow-md shadow-slate-200`}>
                <Icon size={24} />
            </div>
            {trend && (
                <span className="bg-green-100 text-green-700 text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1">
                    {trend}
                </span>
            )}
        </div>
        <div>
            <p className="text-slate-500 text-sm font-medium mb-1">{label}</p>
            <h3 className="text-3xl font-extrabold text-slate-800 tracking-tight">{value}</h3>
        </div>
    </motion.div>
);

const ActionCard = ({ icon: Icon, title, description, onClick, delay }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay }}
        onClick={onClick}
        className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg hover:border-primary/30 hover:bg-slate-50 transition-all cursor-pointer group flex items-start gap-5"
    >
        <div className="p-4 rounded-xl bg-slate-100 text-slate-500 group-hover:bg-primary group-hover:text-white transition-all duration-300 shrink-0">
            <Icon size={24} />
        </div>
        <div>
            <h3 className="text-lg font-bold text-slate-800 group-hover:text-primary transition-colors flex items-center gap-2">
                {title}
                <ArrowRight size={16} className="opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300" />
            </h3>
            <p className="text-slate-500 text-sm leading-relaxed mt-1 group-hover:text-slate-600">
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
            <div className="flex justify-center items-center h-screen bg-slate-50">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="text-center mt-20 p-8 bg-white rounded-2xl shadow-sm max-w-md mx-auto border border-slate-100">
                <p className="text-slate-500 font-medium">Please log in to view the dashboard.</p>
                <button
                    onClick={() => navigate('/login')}
                    className="mt-4 px-6 py-2 bg-primary text-white rounded-xl hover:bg-primary-hover transition-colors font-medium"
                >
                    Go to Login
                </button>
            </div>
        );
    }

    return (
        <PageContainer className="py-8">
            {/* Header / Hero Section */}
            <header className="mb-10 text-center sm:text-left">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="max-w-3xl"
                >
                    <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight mb-3">
                        Welcome back! <span className="text-primary">{user.name.split(' ')[0]}</span>
                    </h1>
                    <p className="text-lg text-slate-500 font-medium leading-relaxed">
                        Here's an overview of your student database and learning analytics.
                    </p>
                </motion.div>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                <StatCard
                    icon={MessageSquare}
                    label="Total Chats"
                    value={user.stats_chat_count || 0}
                    trend="+12%"
                    color="bg-emerald-500"
                    onClick={() => navigate('/chat')}
                />
                <StatCard
                    icon={Zap}
                    label="Words Generated"
                    value={user.stats_words_generated ? (user.stats_words_generated > 1000 ? (user.stats_words_generated / 1000).toFixed(1) + 'k' : user.stats_words_generated) : '0'}
                    trend="+4"
                    color="bg-blue-500"
                    onClick={() => { }}
                />
                <StatCard
                    icon={Clock}
                    label="Active Streak"
                    value={`${user.active_streak || 0} Days`}
                    trend="Keep it up!"
                    color="bg-amber-500"
                    onClick={() => { }}
                />
                <StatCard
                    icon={GraduationCap}
                    label="Role"
                    value={user.role || 'Student'}
                    trend="Active"
                    color="bg-purple-500"
                    onClick={() => { }}
                />
            </div>

            {/* Quick Actions & Profile Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Available Actions - Spans 2 columns */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-2xl font-bold text-slate-800">Quick Actions</h2>
                        <button
                            onClick={handleNewChat}
                            className="text-primary font-semibold hover:text-primary-hover flex items-center gap-1 text-sm bg-primary/10 px-3 py-1.5 rounded-lg transition-colors group"
                        >
                            Start New Query <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <ActionCard
                            icon={Search}
                            title="Query Records"
                            description="Find students by analyzing database records using natural language."
                            onClick={handleNewChat}
                            delay={0.1}
                        />
                        <ActionCard
                            icon={LayoutDashboard}
                            title="Generate Reports"
                            description="Create visual summaries and performance reports instantly."
                            onClick={handleNewChat}
                            delay={0.2}
                        />
                        <ActionCard
                            icon={MessageSquare}
                            title="Analyze Feedback"
                            description="Process student survey data and feedback forms."
                            onClick={handleNewChat}
                            delay={0.3}
                        />
                        <ActionCard
                            icon={Hash}
                            title="Search History"
                            description="Browse through your past search queries and results."
                            onClick={handleSearchHistory}
                            delay={0.4}
                        />
                    </div>
                </div>

                {/* Profile Sidebar - Spans 1 column */}
                <div className="lg:col-span-1">
                    <motion.div
                        className="bg-white/80 backdrop-blur-md border border-slate-200 rounded-3xl p-8 text-center sticky top-24 shadow-sm hover:shadow-md transition-all duration-300"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.5 }}
                    >
                        <div className="relative inline-block mb-4 group">
                            <div className="absolute -inset-1 bg-gradient-to-tr from-primary to-blue-500 rounded-full blur opacity-40 group-hover:opacity-75 transition duration-500"></div>
                            <img
                                src={`https://ui-avatars.com/api/?name=${user.name.replace(' ', '+')}&background=2E8B57&color=fff&size=128`}
                                alt="Profile"
                                className="relative w-24 h-24 rounded-full border-4 border-white shadow-lg mx-auto"
                            />
                            <div className="absolute bottom-1 right-1 w-5 h-5 bg-green-500 border-2 border-white rounded-full"></div>
                        </div>

                        <h3 className="text-xl font-bold text-slate-900 mb-1">{user.name}</h3>
                        <p className="text-slate-500 text-sm mb-6">{user.role === 'admin' ? 'System Administrator' : 'User'}</p>

                        <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
                            <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                                <span className="block text-slate-400 text-xs uppercase font-semibold">Email</span>
                                <span className="font-medium text-slate-700 truncate" title={user.email}>{user.email.split('@')[0]}</span>
                            </div>
                            <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                                <span className="block text-slate-400 text-xs uppercase font-semibold">College</span>
                                <span className="font-medium text-slate-700 truncate" title={user.college}>{user.college || 'N/A'}</span>
                            </div>
                        </div>

                        <button
                            className="w-full flex items-center justify-center gap-2 text-slate-600 hover:text-red-500 hover:bg-red-50 py-3 rounded-xl transition-all font-medium border border-transparent hover:border-red-100 group"
                            onClick={() => {
                                localStorage.removeItem('token');
                                window.location.href = '/login';
                            }}
                        >
                            <LogOut size={18} className="group-hover:translate-x-1 transition-transform" />
                            <span>Sign Out</span>
                        </button>
                    </motion.div>
                </div>
            </div>
        </PageContainer>
    );
}

export default Dashboard;
