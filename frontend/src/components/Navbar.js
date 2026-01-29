import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../App.css';

function Navbar() {
    const location = useLocation();

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    Amypo Assistant
                </Link>
                <div className="navbar-links">
                    <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
                        Dashboard
                    </Link>
                    <Link to="/chat" className={`nav-link ${location.pathname === '/chat' ? 'active' : ''}`}>
                        Chat
                    </Link>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
