import create from 'zustand';

export const useChatStore = create((set) => ({
  messages: [],
  isLoading: false,
  userId: 'user_' + Math.random().toString(36).substr(2, 9),
  darkMode: false,
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  clearMessages: () => set({ messages: [] }),
  
  toggleDarkMode: () => set((state) => ({
    darkMode: !state.darkMode
  })),
  
  setDarkMode: (dark) => set({ darkMode: dark }),
}));

export const useInsightsStore = create((set) => ({
  insights: {
    totalChats: 0,
    symptomFrequency: {},
    recentConditions: [],
    successRate: 0,
  },
  
  setInsights: (insights) => set({ insights }),
}));

export const useRLStore = create((set) => ({
  stats: {
    total_feedback: 0,
    overall_success_rate: 0,
  },
  recommendations: [],
  
  setStats: (stats) => set({ stats }),
  setRecommendations: (recs) => set({ recommendations: recs }),
}));
