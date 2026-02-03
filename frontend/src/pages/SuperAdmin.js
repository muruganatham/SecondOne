import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shield, Activity, Users, MessageSquare, Database, TrendingUp, Clock, CheckCircle } from 'lucide-react';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    BarChart, Bar, PieChart, Pie, Cell, Legend, LineChart, Line
} from 'recharts';
import PageContainer from '../Components/Layout/PageContainer';
import Login from '../Components/Login';

const MetricCard = ({ icon: Icon, title, value, subtext, color, delay, onClick }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay, duration: 0.5 }}
        whileHover={onClick ? { y: -5, cursor: 'pointer' } : {}}
        onClick={onClick}
        className={`bg-white/90 backdrop-blur-sm p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-xl transition-all relative overflow-hidden group ${onClick ? 'cursor-pointer' : ''}`}
    >
        <div className={`absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-5 group-hover:opacity-10 transition-opacity ${color.replace('text-', 'bg-')}`}></div>
        <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-xl ${color.replace('text-', 'bg-').replace('600', '100')} ${color}`}>
                <Icon size={24} />
            </div>
            {subtext && (
                <span className="text-xs font-bold px-2 py-1 rounded-full bg-slate-100 text-slate-600">
                    {subtext}
                </span>
            )}
        </div>
        <div>
            <h3 className="text-slate-500 text-sm font-medium mb-1">{title}</h3>
            <p className="text-3xl font-extrabold text-slate-800 tracking-tight">{value}</p>
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

                const response = await fetch('http://localhost:8000/api/v1/auth/super-admin/metrics', {
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
            <div className="flex justify-center items-center h-screen bg-slate-50">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (error === "auth_required") {
        return (
            <div className="fixed inset-0 z-50 bg-white">
                <Login />
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col justify-center items-center h-screen bg-slate-50 p-6 text-center">
                <div className="bg-red-50 p-6 rounded-xl border border-red-100 mb-4">
                    <Shield size={48} className="text-red-500 mx-auto mb-2" />
                    <h2 className="text-xl font-bold text-slate-800">Connection Failed</h2>
                    <p className="text-slate-500">{error}</p>
                </div>
                <button onClick={() => navigate('/')} className="text-indigo-600 font-medium hover:underline">Return to Dashboard</button>
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
        <PageContainer className="py-8 bg-slate-50/50">
            {/* Header: Cleaned up as requested */}
            <header className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">System Analytics & Reports</h1>
                </motion.div>

                <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-2 rounded-xl border border-emerald-100">
                            <Activity size={18} />
                            <span className="font-medium text-sm">System Health: {metrics.system_health}</span>
                        </div>
                    </div>
                </motion.div>
            </header>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
                <MetricCard icon={Database} title="Total Accuracy Score" value={`${metrics.accuracy_score}%`} subtext="Top Tier" color="text-emerald-600" delay={0.1} />
                <MetricCard icon={Shield} title="SQL Success Rate" value={`${metrics.sql_success_rate}%`} subtext="Valid Queries" color="text-indigo-600" delay={0.15} />
                <MetricCard icon={Clock} title="Avg Response Time" value={`${metrics.avg_response_time}s`} subtext="Latency" color="text-cyan-600" delay={0.2} />
                <MetricCard
                    icon={MessageSquare}
                    title="Total Queries"
                    value={metrics.total_queries.toLocaleString()}
                    subtext="All Time"
                    color="text-blue-600"
                    delay={0.25}
                    onClick={() => navigate('/chat')}
                />
                <MetricCard icon={Users} title="Total Users" value={metrics.total_users.toLocaleString()} subtext={`${metrics.active_users} Active`} color="text-violet-600" delay={0.3} />
                <MetricCard icon={TrendingUp} title="Data Processed" value={(metrics.total_words_generated / 1000).toFixed(1) + 'k'} subtext="Words" color="text-amber-600" delay={0.35} />
            </div>

            {/* Chart Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">

                {/* Accuracy Trend (Area) - Spans 2 cols */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-100 shadow-lg">
                    <h3 className="text-lg font-bold text-slate-800 mb-1">AI Performance Trend</h3>
                    <p className="text-sm text-slate-500 mb-6">Confidence score consistency over time</p>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={accuracyData}>
                                <defs>
                                    <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} stroke="#94a3b8" fontSize={12} />
                                <YAxis axisLine={false} tickLine={false} stroke="#94a3b8" fontSize={12} domain={[80, 100]} />
                                <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                                <Area type="monotone" dataKey="accuracy" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorAcc)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* Topic Distribution (Pie) */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-lg">
                    <h3 className="text-lg font-bold text-slate-800 mb-1">Query Distribution</h3>
                    <p className="text-sm text-slate-500 mb-6">Most queried categories</p>
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
                                >
                                    {topicData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip contentStyle={{ borderRadius: '12px', border: 'none' }} />
                                <Legend verticalAlign="bottom" height={36} iconType="circle" />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            </div>

            {/* Row 2: Engagement & Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* Engagement Bar Chart */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-lg">
                    <h3 className="text-lg font-bold text-slate-800 mb-1">User Engagement</h3>
                    <p className="text-sm text-slate-500 mb-6">Active users vs Queries per day</p>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={engagementData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} stroke="#94a3b8" fontSize={12} />
                                <YAxis axisLine={false} tickLine={false} stroke="#94a3b8" fontSize={12} />
                                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '12px', border: 'none' }} />
                                <Legend />
                                <Bar dataKey="active" name="Active Users" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                                <Bar dataKey="queries" name="Queries" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* Recent Activity Table */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-lg flex flex-col">
                    <h3 className="text-lg font-bold text-slate-800 mb-1">Recent Activity</h3>
                    <p className="text-sm text-slate-500 mb-6">Latest interactions with the AI</p>

                    <div className="flex-1 overflow-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr>
                                    <th className="pb-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">User</th>
                                    <th className="pb-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Topic/Query</th>
                                    <th className="pb-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Status</th>
                                    <th className="pb-4 text-xs font-semibold text-slate-400 uppercase tracking-wider text-right">Date</th>
                                </tr>
                            </thead>
                            <tbody className="text-sm">
                                {recentActivity.length > 0 ? (
                                    recentActivity.map((item) => (
                                        <tr key={item.id} className="border-t border-slate-50 hover:bg-slate-50/50 transition-colors">
                                            <td className="py-3 font-medium text-slate-700">{item.user}</td>
                                            <td className="py-3 text-slate-600 truncate max-w-[150px]">{item.topic}</td>
                                            <td className="py-3">
                                                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700">
                                                    <CheckCircle size={12} />
                                                    {item.status}
                                                </span>
                                            </td>
                                            <td className="py-3 text-right text-slate-400 font-mono text-xs">{item.date}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="4" className="py-8 text-center text-slate-400 italic">No recent activity found</td>
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
