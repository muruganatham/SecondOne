/**
 * Color Theme Constants
 * Centralized color palette for the Amypo Assistant
 */

export const colors = {
    // Primary Brand Colors
    primary: {
        main: '#2E8B57',
        hover: '#256f46',
        light: '#3da66b',
        dark: '#1f5f3d',
    },

    // Background Colors
    background: {
        primary: '#ffffff',
        secondary: '#f8fafc',
        tertiary: '#f1f5f9',
        dark: '#0f172a',
    },

    // Text Colors
    text: {
        primary: '#1e293b',
        secondary: '#64748b',
        light: '#94a3b8',
        inverse: '#f1f5f9',
    },

    // Status Colors
    status: {
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6',
    },

    // UI Elements
    border: '#e2e8f0',
    divider: '#cbd5e1',
    overlay: 'rgba(0, 0, 0, 0.5)',

    // Glassmorphism
    glass: {
        background: 'rgba(255, 255, 255, 0.85)',
        border: 'rgba(46, 139, 87, 0.15)',
    },

    // Chart Colors
    chart: [
        '#2E8B57', // Amypo Green
        '#3498db', // Blue
        '#e74c3c', // Red
        '#f39c12', // Orange
        '#9b59b6', // Purple
        '#1abc9c', // Teal
        '#34495e', // Dark Gray
        '#e67e22', // Dark Orange
    ],

    // Dark Mode (for future use)
    dark: {
        background: {
            primary: '#0f172a',
            secondary: '#1e293b',
            tertiary: '#334155',
        },
        text: {
            primary: '#f1f5f9',
            secondary: '#94a3b8',
            light: '#64748b',
        },
    },
};

export default colors;
