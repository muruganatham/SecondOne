import React from "react";
import { Link } from 'react-router-dom';

function Dashboard() {
    return (
        <div className="dashboard-container">
            <h1>Dashboard</h1>

            <p>
                Welcome to the Amypo Application Dashboard.
            </p>

            <div className="action-area" style={{ marginBottom: '20px' }}>
                <Link to="/chat">
                    <button style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer', backgroundColor: '#61dafb', border: 'none', borderRadius: '5px' }}>
                        Open AI Chat
                    </button>
                </Link>
            </div>

            <div className="dashboard-cards">
                <div className="card">
                    <h3>Total Queries</h3>
                    <p>0</p>
                </div>

                <div className="card">
                    <h3>Last Query</h3>
                    <p>No data</p>
                </div>

                <div className="card">
                    <h3>Status</h3>
                    <p>Active</p>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
