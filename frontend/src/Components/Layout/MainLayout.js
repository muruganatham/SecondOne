import React from 'react';
import Navbar from '../Navbar';

const MainLayout = ({ children, showNavbar = true }) => {
    return (
        <div className="min-h-screen bg-[#050505] relative flex flex-col font-mono text-gray-200 overflow-hidden">
            {/* Animated Background Shapes */}
            <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
                {/* Large gradient orb - top right */}
                <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-[#00ff9d]/5 to-purple-900/10 rounded-full blur-[100px] animate-pulse"></div>

                {/* Medium gradient orb - bottom left */}
                <div className="absolute -bottom-32 -left-32 w-80 h-80 bg-gradient-to-tr from-purple-900/10 to-blue-900/10 rounded-full blur-[100px] animate-pulse" style={{ animationDelay: '2s' }}></div>

                {/* Small accent orb - center */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[radial-gradient(circle_at_center,rgba(0,255,157,0.03)_0%,transparent_70%)] blur-3xl pointer-events-none"></div>
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
