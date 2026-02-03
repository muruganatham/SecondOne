import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shield, Activity, Users, MessageSquare, Database, TrendingUp, Clock, CheckCircle } from 'lucide-react';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    BarChart, Bar, PieChart, Pie, Cell, Legend
} from 'recharts';
import PageContainer from '../Components/Layout/PageContainer';
import Login from '../Components/Login';
import { API_BASE_URL } from '../config';

const MetricCard = ({ icon: Icon, title, value, subtext, color, delay, onClick }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay, duration: 0.5 }}
        whileHover={onClick ? { y: -5, cursor: 'pointer', borderColor: 'rgba(0, 255, 157, 0.5)' } : {}}
        onClick={onClick}
        className={`bg-[#0a0a0a]/90 backdrop-blur-sm p-6 rounded-2xl border border-white/10 shadow-lg hover:shadow-[0_0_20px_rgba(0,255,157,0.1)] transition-all relative overflow-hidden group ${onClick ? 'cursor-pointer' : ''}`}
    >
        <div className={`absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-5 group-hover:opacity-10 transition-opacity ${color.replace('text-', 'bg-')}`}></div>
        <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-xl bg-white/5 ${color} border border-white/5`}>
                <Icon size={24} />
            </div>
            {subtext && (
                <span className="text-[10px] font-bold px-2 py-1 rounded-full bg-white/5 text-gray-400 border border-white/10 uppercase tracking-wider">
                    {subtext}
                </span>
            )}
        </div>
        <div>
            <h3 className="text-gray-500 text-xs font-mono font-medium mb-1 uppercase tracking-wider">{title}</h3>
            <p className="text-3xl font-bold text-white tracking-tight">{value}</p>
        </div>
    </motion.div>
);

function SuperAdmin() {
    const navigate = useNavigate();
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/login');
                    return;
                }

                const response = await fetch(`${API_BASE_URL}/auth/super-admin/metrics`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.status === 403) {
                    setError("auth_required");
                    return;
                }

                if (response.ok) {
                    const data = await response.json();
                    setMetrics(data);
                } else {
                    setError("Failed to load metrics.");
                }
            } catch (err) {
                console.error(err);
                setError("Connection error.");
            } finally {
                setLoading(false);
            }
        };

        fetchMetrics();
    }, [navigate]);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen bg-[#050505]">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#00ff9d]"></div>
            </div>
        );
    }

    if (error === "auth_required") {
        return (
            <div className="fixed inset-0 z-50 bg-[#050505]">
                <Login />
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col justify-center items-center h-screen bg-[#050505] p-6 text-center">
                <div className="bg-red-500/10 p-6 rounded-xl border border-red-500/30 mb-4">
                    <Shield size={48} className="text-red-500 mx-auto mb-2" />
                    <h2 className="text-xl font-bold text-white mb-1">CONNECTION FAILURE</h2>
                    <p className="text-red-400 font-mono text-sm">{error}</p>
                </div>
                <button onClick={() => navigate('/')} className="text-[#00ff9d] font-bold hover:underline font-mono text-sm">RETURN TO TERMINAL</button>
            </div>
        );
    }

    // Use fetched data or defaults
    const accuracyData = [
        { name: 'Mon', accuracy: 88 },
        { name: 'Tue', accuracy: 90 },
        { name: 'Wed', accuracy: 92 },
        { name: 'Thu', accuracy: 89 },
        { name: 'Fri', accuracy: 94 },
        { name: 'Sat', accuracy: 95 },
        { name: 'Sun', accuracy: 96 },
    ];

    const engagementData = metrics.engagement_trend || [];
    const topicData = metrics.topic_distribution || [];
    const recentActivity = metrics.recent_activity || [];

    return (
        <PageContainer className="py-8 bg-[#050505] min-h-screen text-gray-200">
            {/* Header */}
            <header className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
                    <div className="flex items-center gap-3 mb-2">
                        <Shield className="text-[#00ff9d]" size={28} />
                        <h1 className="text-3xl font-extrabold text-white tracking-tight">SYSTEM ADMIN CORE</h1>
                    </div>
                    <p className="text-gray-500 text-sm font-mono">Real-time surveillance and diagnostics.</p>
                </motion.div>

                <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2 bg-[#00ff9d]/5 text-[#00ff9d] px-4 py-2 rounded-xl border border-[#00ff9d]/20 shadow-[0_0_10px_rgba(0,255,157,0.1)]">
                            <Activity size={18} className="animate-pulse" />
                            <span className="font-bold text-sm font-mono tracking-wide">SYSTEM STATUS: {metrics.system_health.toUpperCase()}</span>
                        </div>
                    </div>
                </motion.div>
            </header>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
                <MetricCard icon={Database} title="Model Accuracy" value={`${metrics.accuracy_score}%`} subtext="OPTIMAL" color="text-emerald-400" delay={0.1} />
                <MetricCard icon={Shield} title="SQL Integrity" value={`${metrics.sql_success_rate}%`} subtext="SECURE" color="text-indigo-400" delay={0.15} />
                <MetricCard icon={Clock} title="Latency" value={`${metrics.avg_response_time}s`} subtext="FAST" color="text-cyan-400" delay={0.2} />
                <MetricCard
                    icon={MessageSquare}
                    title="Queries Processed"
                    value={metrics.total_queries.toLocaleString()}
                    subtext="LIFETIME"
                    color="text-blue-400"
                    delay={0.25}
                    onClick={() => navigate('/chat')}
                />
                <MetricCard icon={Users} title="Active Users" value={metrics.total_users.toLocaleString()} subtext={`${metrics.active_users} ONLINE`} color="text-violet-400" delay={0.3} />
                <MetricCard icon={TrendingUp} title="Data Throughput" value={(metrics.total_words_generated / 1000).toFixed(1) + 'k'} subtext="TOKENS" color="text-amber-400" delay={0.35} />
            </div>

            {/* Chart Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">

                {/* Accuracy Trend (Area) - Spans 2 cols */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="lg:col-span-2 bg-[#0a0a0a]/90 backdrop-blur-sm p-6 rounded-2xl border border-white/10 shadow-lg">
                    <h3 className="text-lg font-bold text-white mb-1">Performance Vector</h3>
                    <p className="text-xs text-gray-500 font-mono mb-6 uppercase tracking-wider">Confidence Score Variance</p>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={accuracyData}>
                                <defs>
                                    <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#00ff9d" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="#00ff9d" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#333" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} stroke="#666" fontSize={12} />
                                <YAxis axisLine={false} tickLine={false} stroke="#666" fontSize={12} domain={[80, 100]} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#050505', borderRadius: '12px', border: '1px solid #333', color: '#fff' }}
                                    itemStyle={{ color: '#00ff9d' }}
                                />
                                <Area type="monotone" dataKey="accuracy" stroke="#00ff9d" strokeWidth={2} fillOpacity={1} fill="url(#colorAcc)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* Topic Distribution (Pie) */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }} className="bg-[#0a0a0a]/90 backdrop-blur-sm p-6 rounded-2xl border border-white/10 shadow-lg">
                    <h3 className="text-lg font-bold text-white mb-1">Query Taxonomy</h3>
                    <p className="text-xs text-gray-500 font-mono mb-6 uppercase tracking-wider">Subject Classification</p>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={topicData}
                                    cx="50%" cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                    stroke="none"
                                >
                                    {topicData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip contentStyle={{ backgroundColor: '#050505', borderRadius: '12px', border: '1px solid #333' }} />
                                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ color: '#999', fontSize: '12px' }} />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            </div>

            {/* Row 2: Engagement & Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* Engagement Bar Chart */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="bg-[#0a0a0a]/90 backdrop-blur-sm p-6 rounded-2xl border border-white/10 shadow-lg">
                    <h3 className="text-lg font-bold text-white mb-1">Traffic Analysis</h3>
                    <p className="text-xs text-gray-500 font-mono mb-6 uppercase tracking-wider">User Sessions vs Query Volume</p>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={engagementData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#333" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} stroke="#666" fontSize={12} />
                                <YAxis axisLine={false} tickLine={false} stroke="#666" fontSize={12} />
                                <Tooltip cursor={{ fill: '#ffffff05' }} contentStyle={{ backgroundColor: '#050505', borderRadius: '12px', border: '1px solid #333' }} />
                                <Legend wrapperStyle={{ color: '#999', fontSize: '12px', paddingTop: '10px' }} />
                                <Bar dataKey="active" name="Active Sessions" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                                <Bar dataKey="queries" name="Query Load" fill="#00ff9d" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* Recent Activity Table */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }} className="bg-[#0a0a0a]/90 backdrop-blur-sm p-6 rounded-2xl border border-white/10 shadow-lg flex flex-col">
                    <h3 className="text-lg font-bold text-white mb-1">Live Feed</h3>
                    <p className="text-xs text-gray-500 font-mono mb-6 uppercase tracking-wider">Recent System Interactions</p>

                    <div className="flex-1 overflow-auto custom-scrollbar">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr>
                                    <th className="pb-4 text-xs font-bold text-gray-500 uppercase tracking-wider font-mono">User ID</th>
                                    <th className="pb-4 text-xs font-bold text-gray-500 uppercase tracking-wider font-mono">Query Packet</th>
                                    <th className="pb-4 text-xs font-bold text-gray-500 uppercase tracking-wider font-mono">Status</th>
                                    <th className="pb-4 text-xs font-bold text-gray-500 uppercase tracking-wider font-mono text-right">Timestamp</th>
                                </tr>
                            </thead>
                            <tbody className="text-sm">
                                {recentActivity.length > 0 ? (
                                    recentActivity.map((item) => (
                                        <tr key={item.id} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                                            <td className="py-3 font-medium text-gray-300 font-mono text-xs">{item.user}</td>
                                            <td className="py-3 text-gray-400 truncate max-w-[150px] font-mono text-xs">{item.topic}</td>
                                            <td className="py-3">
                                                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold bg-[#00ff9d]/10 text-[#00ff9d] border border-[#00ff9d]/20 uppercase tracking-wider">
                                                    <CheckCircle size={10} />
                                                    {item.status}
                                                </span>
                                            </td>
                                            <td className="py-3 text-right text-gray-600 font-mono text-[10px]">{item.date}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="4" className="py-8 text-center text-gray-600 italic font-mono text-xs">NO DATA STREAM DETECTED</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </motion.div>
            </div>
        </PageContainer>
    );
}

export default SuperAdmin;
