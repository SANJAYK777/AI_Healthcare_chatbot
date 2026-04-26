import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const chatAPI = {
  sendMessage: async (content, userId) => {
    try {
      const response = await api.post('/chat', {
        content,
        user_id: userId,
      });
      return response.data;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  },

  submitFeedback: async (messageId, isHelpful, category, comment) => {
    try {
      const response = await api.post('/feedback', {
        message_id: messageId,
        is_helpful: isHelpful,
        category: category || 'general',
        comment: comment || null,
      });
      return response.data;
    } catch (error) {
      console.error('Feedback error:', error);
      throw error;
    }
  },

  getHistory: async (userId, limit = 50) => {
    try {
      const response = await api.post('/history', {
        user_id: userId,
        limit,
      });
      return response.data;
    } catch (error) {
      console.error('History error:', error);
      throw error;
    }
  },

  getInsights: async () => {
    try {
      const response = await api.get('/insights');
      return response.data;
    } catch (error) {
      console.error('Insights error:', error);
      throw error;
    }
  },

  getSecurityStatus: async () => {
    try {
      const response = await api.get('/security/status');
      return response.data;
    } catch (error) {
      console.error('Security status error:', error);
      throw error;
    }
  },

  getRLStats: async () => {
    try {
      const response = await api.get('/rl-stats');
      return response.data;
    } catch (error) {
      console.error('RL stats error:', error);
      throw error;
    }
  },

  getRLRecommendations: async () => {
    try {
      const response = await api.get('/rl-recommendations');
      return response.data;
    } catch (error) {
      console.error('RL recommendations error:', error);
      throw error;
    }
  },

  clearHistory: async (userId) => {
    try {
      const response = await api.post('/settings/clear-history', null, {
        params: { user_id: userId }
      });
      return response.data;
    } catch (error) {
      console.error('Clear history error:', error);
      throw error;
    }
  },

  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  },
};

export default api;
