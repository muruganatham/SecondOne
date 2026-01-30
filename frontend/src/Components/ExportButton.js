import React, { useState } from 'react';
import { Download, FileText, FileSpreadsheet, FileJson, ChevronDown } from 'lucide-react';
import { exportWithTimestamp } from '../utils/exportUtils';
import './ExportButton.css';

function ExportButton({ data, filename = 'query_results' }) {
    const [isOpen, setIsOpen] = useState(false);

    if (!data || data.length === 0) {
        return null;
    }

    const handleExport = (format) => {
        exportWithTimestamp(data, format, filename);
        setIsOpen(false);
    };

    return (
        <div className="export-button-container">
            <button
                className="export-button"
                onClick={() => setIsOpen(!isOpen)}
            >
                <Download size={16} />
                <span>Export</span>
                <ChevronDown size={14} className={`chevron ${isOpen ? 'open' : ''}`} />
            </button>

            {isOpen && (
                <>
                    <div className="export-backdrop" onClick={() => setIsOpen(false)} />
                    <div className="export-dropdown">
                        <button
                            className="export-option"
                            onClick={() => handleExport('csv')}
                        >
                            <FileSpreadsheet size={16} />
                            <div className="export-option-text">
                                <span className="export-option-title">Export as CSV</span>
                                <span className="export-option-desc">Comma-separated values</span>
                            </div>
                        </button>

                        <button
                            className="export-option"
                            onClick={() => handleExport('excel')}
                        >
                            <FileSpreadsheet size={16} color="#217346" />
                            <div className="export-option-text">
                                <span className="export-option-title">Export as Excel</span>
                                <span className="export-option-desc">Microsoft Excel (.xlsx)</span>
                            </div>
                        </button>

                        <button
                            className="export-option"
                            onClick={() => handleExport('json')}
                        >
                            <FileJson size={16} color="#f39c12" />
                            <div className="export-option-text">
                                <span className="export-option-title">Export as JSON</span>
                                <span className="export-option-desc">JavaScript Object Notation</span>
                            </div>
                        </button>

                        <button
                            className="export-option"
                            onClick={() => handleExport('txt')}
                        >
                            <FileText size={16} />
                            <div className="export-option-text">
                                <span className="export-option-title">Export as TXT</span>
                                <span className="export-option-desc">Plain text table</span>
                            </div>
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

export default ExportButton;
