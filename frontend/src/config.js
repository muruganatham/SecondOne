// Dynamic API URL configuration
// Automatically detects the host IP to allow LAN access
const getApiBaseUrl = () => {
    const hostname = window.location.hostname;
    return `http://${hostname}:8000/api/v1`;
};

export const API_BASE_URL = getApiBaseUrl();
