/**
 * Spacing Scale
 * Consistent spacing values throughout the application
 */

export const spacing = {
    // Base spacing scale (in pixels)
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
    '3xl': '64px',
    '4xl': '96px',

    // Component-specific spacing
    component: {
        padding: {
            xs: '8px 12px',
            sm: '10px 16px',
            md: '12px 20px',
            lg: '16px 24px',
        },
        margin: {
            xs: '8px',
            sm: '12px',
            md: '16px',
            lg: '24px',
        },
        gap: {
            xs: '4px',
            sm: '8px',
            md: '12px',
            lg: '16px',
        },
    },

    // Border radius
    radius: {
        sm: '6px',
        md: '8px',
        lg: '12px',
        xl: '16px',
        full: '9999px',
    },

    // Shadows
    shadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
    },
};

export default spacing;
