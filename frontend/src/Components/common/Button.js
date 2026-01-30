import React from 'react';
import './Button.css';

function Button({
    children,
    variant = 'primary', // primary, secondary, ghost, danger
    size = 'md', // sm, md, lg
    fullWidth = false,
    disabled = false,
    loading = false,
    icon,
    iconPosition = 'left', // left, right
    onClick,
    type = 'button',
    className = '',
    ...props
}) {
    const buttonClasses = [
        'btn',
        `btn-${variant}`,
        `btn-${size}`,
        fullWidth && 'btn-full-width',
        loading && 'btn-loading',
        disabled && 'btn-disabled',
        className,
    ].filter(Boolean).join(' ');

    return (
        <button
            type={type}
            className={buttonClasses}
            onClick={onClick}
            disabled={disabled || loading}
            {...props}
        >
            {loading && (
                <span className="btn-spinner">
                    <span className="spinner-dot"></span>
                    <span className="spinner-dot"></span>
                    <span className="spinner-dot"></span>
                </span>
            )}
            {!loading && icon && iconPosition === 'left' && (
                <span className="btn-icon btn-icon-left">{icon}</span>
            )}
            <span className="btn-text">{children}</span>
            {!loading && icon && iconPosition === 'right' && (
                <span className="btn-icon btn-icon-right">{icon}</span>
            )}
        </button>
    );
}

export default Button;
