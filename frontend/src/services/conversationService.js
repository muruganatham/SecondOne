import { API_BASE_URL } from '../config';

const API_BASE = API_BASE_URL;

export const conversationService = {
    async getAll() {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/conversations/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }
        if (!response.ok) throw new Error('Failed to fetch conversations');
        return response.json();
    },

    async getById(id) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/conversations/${id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }
        if (!response.ok) throw new Error('Failed to fetch conversation');
        return response.json();
    },

    async create(conversation) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/conversations/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(conversation)
        });
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }
        if (!response.ok) throw new Error('Failed to create conversation');
        return response.json();
    },

    async update(id, conversation) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/conversations/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(conversation)
        });
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }
        if (!response.ok) throw new Error('Failed to update conversation');
        return response.json();
    },

    async delete(id) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/conversations/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }
        if (!response.ok) throw new Error('Failed to delete conversation');
        if (response.status === 204) return true;
        return response.json();
    }
};
