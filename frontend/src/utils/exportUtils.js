import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

/**
 * Export Utilities
 * Provides functions to export data in various formats
 */

// Export as CSV
export const exportToCSV = (data, filename = 'export') => {
    if (!data || data.length === 0) {
        console.error('No data to export');
        return;
    }

    const keys = Object.keys(data[0]);

    // Create CSV header
    const header = keys.join(',');

    // Create CSV rows
    const rows = data.map(row => {
        return keys.map(key => {
            const value = row[key];
            // Escape commas and quotes
            if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                return `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        }).join(',');
    });

    // Combine header and rows
    const csv = [header, ...rows].join('\n');

    // Create blob and download
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `${filename}.csv`);
};

// Export as Excel
export const exportToExcel = (data, filename = 'export') => {
    if (!data || data.length === 0) {
        console.error('No data to export');
        return;
    }

    // Create worksheet from data
    const worksheet = XLSX.utils.json_to_sheet(data);

    // Create workbook
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

    // Generate Excel file
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });

    // Create blob and download
    const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, `${filename}.xlsx`);
};

// Export as JSON
export const exportToJSON = (data, filename = 'export') => {
    if (!data || data.length === 0) {
        console.error('No data to export');
        return;
    }

    // Pretty print JSON
    const json = JSON.stringify(data, null, 2);

    // Create blob and download
    const blob = new Blob([json], { type: 'application/json;charset=utf-8;' });
    saveAs(blob, `${filename}.json`);
};

// Export as TXT (formatted table)
export const exportToTXT = (data, filename = 'export') => {
    if (!data || data.length === 0) {
        console.error('No data to export');
        return;
    }

    const keys = Object.keys(data[0]);

    // Calculate column widths
    const columnWidths = keys.map(key => {
        const maxLength = Math.max(
            key.length,
            ...data.map(row => String(row[key]).length)
        );
        return Math.min(maxLength + 2, 30); // Max width 30
    });

    // Create header
    const header = keys.map((key, i) => key.padEnd(columnWidths[i])).join(' | ');
    const separator = columnWidths.map(width => '-'.repeat(width)).join('-+-');

    // Create rows
    const rows = data.map(row => {
        return keys.map((key, i) => {
            const value = String(row[key]);
            return value.padEnd(columnWidths[i]);
        }).join(' | ');
    });

    // Combine all
    const txt = [header, separator, ...rows].join('\n');

    // Create blob and download
    const blob = new Blob([txt], { type: 'text/plain;charset=utf-8;' });
    saveAs(blob, `${filename}.txt`);
};

// Export with timestamp
export const exportWithTimestamp = (data, format, baseName = 'query_results') => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    const filename = `${baseName}_${timestamp}`;

    switch (format.toLowerCase()) {
        case 'csv':
            exportToCSV(data, filename);
            break;
        case 'excel':
        case 'xlsx':
            exportToExcel(data, filename);
            break;
        case 'json':
            exportToJSON(data, filename);
            break;
        case 'txt':
        case 'text':
            exportToTXT(data, filename);
            break;
        default:
            console.error('Unsupported format:', format);
    }
};
