import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, ArrowRight, Eye, EyeOff } from 'lucide-react';
import logo from '../assets/logo.png';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/login', {
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
                // Redirect to dashboard
                navigate('/');
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
        <div className="min-h-screen bg-slate-100 flex items-center justify-center p-4 relative overflow-hidden">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="bg-white/80 backdrop-blur-md p-8 rounded-3xl shadow-xl w-full max-w-md relative z-10 border border-slate-200"
            >
                {/* Logo Section */}
                <div className="text-center mb-8">
                    <motion.img
                        src={logo}
                        alt="Amypo Logo"
                        className="h-12 mx-auto mb-4"
                        initial={{ scale: 0.8 }}
                        animate={{ scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    />
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4 }}
                        className="text-slate-500 text-sm"
                    >
                        Welcome back! Please login to your account.
                    </motion.p>
                </div>

                {/* Form Section */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="relative">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" size={20} />
                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-slate-800 placeholder-slate-400"
                        />
                    </div>

                    <div className="relative">
                        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" size={20} />
                        <input
                            type={showPassword ? "text" : "password"}
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full pl-10 pr-12 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-slate-800 placeholder-slate-400"
                        />
                        <button
                            type="button"
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full py-3 bg-primary text-white rounded-xl font-medium shadow-lg shadow-primary/30 hover:shadow-primary/50 flex items-center justify-center gap-2 mt-6 transition-all"
                        type="submit"
                        style={{ marginTop: '1.5rem' }}
                    >
                        <span>Sign In</span>
                        <ArrowRight size={20} />
                    </motion.button>
                </form>
            </motion.div>

            {/* Animated Background Shapes */}
            <div className="absolute top-0 left-0 w-64 h-64 bg-primary/30 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
            <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse delay-75"></div>
            <div className="absolute -bottom-32 left-20 w-64 h-64 bg-green-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse delay-150"></div>
        </div>
    );
}

export default Login;