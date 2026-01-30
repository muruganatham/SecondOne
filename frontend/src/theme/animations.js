/**
 * Animation Constants
 * Reusable animation configurations
 */

export const animations = {
    // Durations (in milliseconds)
    duration: {
        fast: 150,
        normal: 250,
        slow: 350,
    },

    // Easing Functions
    easing: {
        easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
        easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
        easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
        spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    },

    // Framer Motion Variants
    fadeIn: {
        initial: { opacity: 0 },
        animate: { opacity: 1 },
        exit: { opacity: 0 },
    },

    slideUp: {
        initial: { opacity: 0, y: 20 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: -20 },
    },

    slideDown: {
        initial: { opacity: 0, y: -20 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: 20 },
    },

    scale: {
        initial: { opacity: 0, scale: 0.9 },
        animate: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.9 },
    },

    // CSS Transitions
    transition: {
        all: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
        colors: 'color 0.2s, background-color 0.2s, border-color 0.2s',
        transform: 'transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    },
};

export default animations;
