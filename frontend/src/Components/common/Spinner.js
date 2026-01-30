import React from 'react';
import './Spinner.css';

function Spinner({
    size = 'md', // sm, md, lg
    color = 'primary', // primary, white, secondary
    className = ''
}) {
    return (
        <div className={`spinner-container ${className}`}>
            <div className={`spinner spinner-${size} spinner-${color}`}>
                <div className="spinner-circle"></div>
                <div className="spinner-circle"></div>
                <div className="spinner-circle"></div>
            </div>
        </div>
    );
}

export default Spinner;
