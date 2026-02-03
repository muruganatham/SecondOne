import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, ArrowRight, Eye, EyeOff, Terminal } from 'lucide-react';
import logo from '../assets/logo.png';

import { API_BASE_URL } from '../config';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                console.log('Login successful:', data);
                // Store token
                localStorage.setItem('token', data.access_token);
                // Redirect based on role
                if (data.role_id === 1) {
                    navigate('/super-admin');
                } else {
                    navigate('/');
                }
            } else {
                console.error('Login failed:', data.detail);
                alert(data.detail || 'Login failed. Please check your credentials.');
            }
        } catch (error) {
            console.error('Error during login:', error);
            alert('An error occurred. Please try again later.');
        }
    };

    return (
        <div className="min-h-screen bg-[#050505] flex items-center justify-center p-4 relative overflow-hidden font-mono">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="bg-[#0a0a0a]/80 backdrop-blur-xl p-8 rounded-3xl shadow-2xl w-full max-w-md relative z-10 border border-white/10"
            >
                {/* Logo Section */}
                <div className="text-center mb-8">
                    <motion.div
                        className="mx-auto w-16 h-16 bg-[#00ff9d]/10 rounded-2xl flex items-center justify-center border border-[#00ff9d]/30 mb-4 text-[#00ff9d]"
                        initial={{ scale: 0.8 }}
                        animate={{ scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    >
                        <Terminal size={32} />
                    </motion.div>
                    <motion.h1
                        className="text-2xl font-bold text-white tracking-wider"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                    >
                        SYSTEM_LOGIN
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4 }}
                        className="text-gray-500 text-xs mt-2 uppercase tracking-widest"
                    >
                        Enter Credentials for Access
                    </motion.p>
                </div>

                {/* Form Section */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="relative">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none" size={20} />
                        <input
                            type="email"
                            placeholder="OPERATOR ID / EMAIL"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full pl-10 pr-4 py-3 bg-[#111] border border-white/10 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#00ff9d] focus:border-[#00ff9d] transition-all text-gray-200 placeholder-gray-600 text-sm"
                        />
                    </div>

                    <div className="relative">
                        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none" size={20} />
                        <input
                            type={showPassword ? "text" : "password"}
                            placeholder="ACCESS KEY"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full pl-10 pr-12 py-3 bg-[#111] border border-white/10 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#00ff9d] focus:border-[#00ff9d] transition-all text-gray-200 placeholder-gray-600 text-sm"
                        />
                        <button
                            type="button"
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full py-3 bg-[#00ff9d] text-black rounded-xl font-bold shadow-[0_0_20px_rgba(0,255,157,0.3)] hover:shadow-[0_0_30px_rgba(0,255,157,0.5)] hover:bg-[#00cc7d] flex items-center justify-center gap-2 mt-6 transition-all"
                        type="submit"
                        style={{ marginTop: '1.5rem' }}
                    >
                        <span>INITIATE SESSION</span>
                        <ArrowRight size={20} strokeWidth={2.5} />
                    </motion.button>
                </form>
            </motion.div>

            {/* Animated Background Shapes */}
            <div className="absolute top-0 left-0 w-96 h-96 bg-[#00ff9d]/5 rounded-full filter blur-[100px] animate-pulse"></div>
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-900/10 rounded-full filter blur-[100px] animate-pulse delay-75"></div>
        </div>
    );
}

export default Login;