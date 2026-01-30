import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { BarChart3, LineChart as LineChartIcon, PieChart as PieChartIcon, Table as TableIcon } from 'lucide-react';
import ExportButton from './ExportButton';
import './DataVisualization.css';

const COLORS = ['#2E8B57', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e67e22'];

function DataVisualization({ data, sql }) {
    const [chartType, setChartType] = React.useState('auto');
    const [selectedChart, setSelectedChart] = React.useState(null);

    React.useEffect(() => {
        if (data && data.length > 0) {
            const detected = detectBestChart(data);
            setSelectedChart(detected);
        }
    }, [data]);

    if (!data || data.length === 0) {
        return null;
    }

    // Detect best chart type based on data structure
    const detectBestChart = (data) => {
        const keys = Object.keys(data[0]);
        const numericKeys = keys.filter(key =>
            data.every(row => typeof row[key] === 'number' || !isNaN(parseFloat(row[key])))
        );

        // If only 1-2 rows and has numeric data → Pie Chart
        if (data.length <= 5 && numericKeys.length >= 1) {
            return 'pie';
        }

        // If has date/time column → Line Chart
        const hasTimeColumn = keys.some(key =>
            key.toLowerCase().includes('date') ||
            key.toLowerCase().includes('time') ||
            key.toLowerCase().includes('year') ||
            key.toLowerCase().includes('month')
        );
        if (hasTimeColumn && numericKeys.length >= 1) {
            return 'line';
        }

        // If has categorical data with numbers → Bar Chart
        if (numericKeys.length >= 1 && keys.length >= 2) {
            return 'bar';
        }

        // Default to table for complex data
        return 'table';
    };

    const currentChart = chartType === 'auto' ? selectedChart : chartType;

    // Prepare data for charts
    const prepareChartData = () => {
        return data.map(row => {
            const newRow = {};
            Object.keys(row).forEach(key => {
                // Convert numeric strings to numbers
                const value = row[key];
                newRow[key] = !isNaN(parseFloat(value)) ? parseFloat(value) : value;
            });
            return newRow;
        });
    };

    const chartData = prepareChartData();
    const keys = Object.keys(data[0]);
    const numericKeys = keys.filter(key =>
        chartData.every(row => typeof row[key] === 'number')
    );
    const labelKey = keys.find(key => !numericKeys.includes(key)) || keys[0];

    return (
        <div className="data-visualization">
            {/* Chart Type Selector */}
            <div className="chart-controls">
                <div className="chart-type-selector">
                    <button
                        className={chartType === 'auto' ? 'active' : ''}
                        onClick={() => setChartType('auto')}
                        title="Auto-detect best chart"
                    >
                        Auto
                    </button>
                    <button
                        className={chartType === 'bar' ? 'active' : ''}
                        onClick={() => setChartType('bar')}
                        title="Bar Chart"
                    >
                        <BarChart3 size={16} />
                    </button>
                    <button
                        className={chartType === 'line' ? 'active' : ''}
                        onClick={() => setChartType('line')}
                        title="Line Chart"
                    >
                        <LineChartIcon size={16} />
                    </button>
                    <button
                        className={chartType === 'pie' ? 'active' : ''}
                        onClick={() => setChartType('pie')}
                        title="Pie Chart"
                    >
                        <PieChartIcon size={16} />
                    </button>
                    <button
                        className={chartType === 'table' ? 'active' : ''}
                        onClick={() => setChartType('table')}
                        title="Table View"
                    >
                        <TableIcon size={16} />
                    </button>
                </div>
                <div className="chart-info">
                    {chartType === 'auto' && (
                        <span className="auto-badge">Auto: {selectedChart}</span>
                    )}
                    <ExportButton data={data} filename="query_results" />
                </div>
            </div>

            {/* Chart Rendering */}
            <div className="chart-container">
                {currentChart === 'bar' && (
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                            <XAxis dataKey={labelKey} stroke="#64748b" />
                            <YAxis stroke="#64748b" />
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--bg-secondary)',
                                    border: '1px solid var(--border)',
                                    borderRadius: '8px'
                                }}
                            />
                            <Legend />
                            {numericKeys.map((key, index) => (
                                <Bar
                                    key={key}
                                    dataKey={key}
                                    fill={COLORS[index % COLORS.length]}
                                    radius={[8, 8, 0, 0]}
                                />
                            ))}
                        </BarChart>
                    </ResponsiveContainer>
                )}

                {currentChart === 'line' && (
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                            <XAxis dataKey={labelKey} stroke="#64748b" />
                            <YAxis stroke="#64748b" />
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--bg-secondary)',
                                    border: '1px solid var(--border)',
                                    borderRadius: '8px'
                                }}
                            />
                            <Legend />
                            {numericKeys.map((key, index) => (
                                <Line
                                    key={key}
                                    type="monotone"
                                    dataKey={key}
                                    stroke={COLORS[index % COLORS.length]}
                                    strokeWidth={2}
                                    dot={{ r: 4 }}
                                />
                            ))}
                        </LineChart>
                    </ResponsiveContainer>
                )}

                {currentChart === 'pie' && numericKeys.length > 0 && (
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={chartData}
                                dataKey={numericKeys[0]}
                                nameKey={labelKey}
                                cx="50%"
                                cy="50%"
                                outerRadius={100}
                                label
                            >
                                {chartData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip
                                contentStyle={{
                                    background: 'var(--bg-secondary)',
                                    border: '1px solid var(--border)',
                                    borderRadius: '8px'
                                }}
                            />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                )}

                {currentChart === 'table' && (
                    <div className="data-table-container">
                        <table className="data-table">
                            <thead>
                                <tr>
                                    {keys.map(key => (
                                        <th key={key}>{key}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {data.map((row, index) => (
                                    <tr key={index}>
                                        {keys.map(key => (
                                            <td key={key}>{row[key]}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Data Summary */}
            <div className="data-summary">
                <span>{data.length} rows</span>
                <span>•</span>
                <span>{keys.length} columns</span>
            </div>
        </div>
    );
}

export default DataVisualization;
