import React from 'react';
import './Skeleton.css';

function Skeleton({
    width = '100%',
    height = '20px',
    borderRadius = '8px',
    variant = 'rectangular', // rectangular, circular, text
    animation = 'shimmer', // shimmer, pulse, none
    count = 1,
    className = ''
}) {
    const skeletons = Array.from({ length: count }, (_, index) => (
        <div
            key={index}
            className={`skeleton skeleton-${variant} skeleton-${animation} ${className}`}
            style={{
                width,
                height: variant === 'text' ? '1em' : height,
                borderRadius: variant === 'circular' ? '50%' : borderRadius,
                marginBottom: count > 1 && index < count - 1 ? '8px' : '0',
            }}
        />
    ));

    return count > 1 ? <div className="skeleton-group">{skeletons}</div> : skeletons;
}

export default Skeleton;
