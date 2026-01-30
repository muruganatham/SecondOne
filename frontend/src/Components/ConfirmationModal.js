import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, X } from 'lucide-react';
import './ConfirmationModal.css';

function ConfirmationModal({ isOpen, onClose, onConfirm, sql, affectedRows, queryType }) {
    if (!isOpen) return null;

    const getQueryTypeInfo = () => {
        const sqlUpper = sql.toUpperCase().trim();

        if (sqlUpper.startsWith('UPDATE')) {
            return {
                type: 'UPDATE',
                color: '#f39c12',
                message: 'This will modify existing data',
                icon: '✏️'
            };
        } else if (sqlUpper.startsWith('DELETE')) {
            return {
                type: 'DELETE',
                color: '#e74c3c',
                message: 'This will permanently delete data',
                icon: '🗑️'
            };
        } else if (sqlUpper.startsWith('DROP')) {
            return {
                type: 'DROP',
                color: '#c0392b',
                message: 'This will permanently drop a table/database',
                icon: '⚠️'
            };
        } else if (sqlUpper.startsWith('TRUNCATE')) {
            return {
                type: 'TRUNCATE',
                color: '#e67e22',
                message: 'This will delete all rows from the table',
                icon: '🧹'
            };
        } else if (sqlUpper.startsWith('INSERT')) {
            return {
                type: 'INSERT',
                color: '#27ae60',
                message: 'This will add new data',
                icon: '➕'
            };
        } else if (sqlUpper.startsWith('ALTER')) {
            return {
                type: 'ALTER',
                color: '#8e44ad',
                message: 'This will modify the table structure',
                icon: '🔧'
            };
        }

        return {
            type: 'MODIFY',
            color: '#95a5a6',
            message: 'This will modify your database',
            icon: '⚙️'
        };
    };

    const queryInfo = getQueryTypeInfo();

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        className="confirmation-backdrop"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                    />

                    {/* Modal */}
                    <motion.div
                        className="confirmation-modal"
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        transition={{ type: 'spring', duration: 0.3 }}
                    >
                        {/* Header */}
                        <div className="modal-header" style={{ borderLeftColor: queryInfo.color }}>
                            <div className="modal-title-section">
                                <div className="modal-icon" style={{ background: queryInfo.color }}>
                                    <AlertTriangle size={24} color="white" />
                                </div>
                                <div>
                                    <h2 className="modal-title">Confirm {queryInfo.type} Operation</h2>
                                    <p className="modal-subtitle">{queryInfo.message}</p>
                                </div>
                            </div>
                            <button className="modal-close" onClick={onClose}>
                                <X size={20} />
                            </button>
                        </div>

                        {/* Body */}
                        <div className="modal-body">
                            {/* Warning Box */}
                            <div className="warning-box" style={{ borderColor: queryInfo.color }}>
                                <span className="warning-icon">{queryInfo.icon}</span>
                                <div>
                                    <strong>Warning:</strong> This action will affect your database.
                                    {affectedRows > 0 && (
                                        <span className="affected-rows">
                                            {' '}Approximately <strong>{affectedRows} row(s)</strong> will be affected.
                                        </span>
                                    )}
                                </div>
                            </div>

                            {/* SQL Preview */}
                            <div className="sql-preview">
                                <div className="sql-preview-header">
                                    <span>SQL Query to Execute:</span>
                                </div>
                                <pre className="sql-code">{sql}</pre>
                            </div>

                            {/* Info */}
                            <div className="modal-info">
                                <p>Please review the query carefully before proceeding.</p>
                                <p className="modal-note">
                                    💡 <strong>Tip:</strong> Make sure you have a backup before modifying data.
                                </p>
                            </div>
                        </div>

                        {/* Footer */}
                        <div className="modal-footer">
                            <button className="btn-cancel" onClick={onClose}>
                                Cancel
                            </button>
                            <button
                                className="btn-confirm"
                                onClick={onConfirm}
                                style={{ background: queryInfo.color }}
                            >
                                Confirm {queryInfo.type}
                            </button>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}

export default ConfirmationModal;
