import React from 'react';
import './Card.css';

function Card({
    children,
    hover = false,
    shadow = 'md', // sm, md, lg, none
    padding = 'md', // sm, md, lg, none
    borderRadius = 'md', // sm, md, lg
    className = '',
    onClick,
    ...props
}) {
    const cardClasses = [
        'card',
        hover && 'card-hover',
        `card-shadow-${shadow}`,
        `card-padding-${padding}`,
        `card-radius-${borderRadius}`,
        onClick && 'card-clickable',
        className,
    ].filter(Boolean).join(' ');

    return (
        <div className={cardClasses} onClick={onClick} {...props}>
            {children}
        </div>
    );
}

export default Card;
