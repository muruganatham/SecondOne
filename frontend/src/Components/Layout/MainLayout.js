import React from 'react';
import Navbar from '../Navbar';

const MainLayout = ({ children, showNavbar = true }) => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 relative flex flex-col font-sans text-slate-900 overflow-hidden">
            {/* Animated Background Shapes */}
            <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
                {/* Large gradient orb - top right */}
                <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-purple-400/30 to-pink-400/30 rounded-full blur-3xl animate-pulse"></div>

                {/* Medium gradient orb - bottom left */}
                <div className="absolute -bottom-32 -left-32 w-80 h-80 bg-gradient-to-tr from-blue-400/30 to-indigo-400/30 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>

                {/* Small accent orb - center */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-gradient-to-br from-violet-400/20 to-fuchsia-400/20 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '2s' }}></div>
            </div>

            {/* Content */}
            <div className="relative z-10 flex flex-col min-h-screen">
                {showNavbar && <Navbar />}
                <main className="flex-1 flex flex-col">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default MainLayout;
