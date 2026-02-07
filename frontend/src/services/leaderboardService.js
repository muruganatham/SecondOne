import { API_BASE_URL } from '../config';

const leaderboardService = {
    /**
     * Fetch leaderboard data
     * @param {Object} filters - filters like college_id, course_id, limit, category, batch_id, section_id, department_id
     */
    async getLeaderboard(filters) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/analytics/leaderboard`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(filters)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to fetch leaderboard data');
        }

        return await response.json();
    },

    /**
     * Fetch all available courses for a college
     * @param {number} collegeId - Optional college ID
     */
    async getCourses(collegeId = null) {
        const token = localStorage.getItem('token');
        let url = `${API_BASE_URL}/analytics/leaderboard/courses`;
        if (collegeId) {
            url += `?college_id=${collegeId}`;
        }

        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Failed to fetch courses');
        return await response.json();
    },

    /**
     * Fetch list of colleges (SuperAdmin only)
     */
    async getColleges() {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/analytics/leaderboard/colleges`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch colleges');
        return await response.json();
    },

    /**
     * Fetch metadata (batches, sections, departments) for a college
     * @param {number} collegeId 
     */
    async getMetadata(collegeId) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/analytics/leaderboard/metadata?college_id=${collegeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch metadata');
        return await response.json();
    }
};

export default leaderboardService;
