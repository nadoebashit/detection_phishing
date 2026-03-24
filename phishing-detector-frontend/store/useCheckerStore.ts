import { create } from 'zustand';
import { CheckResult } from '../lib/types';
import { api } from '../lib/api';

interface CheckerStore {
  currentResult: CheckResult | null;
  isLoading: boolean;
  error: string | null;
  history: CheckResult[];
  checkURL: (url: string) => Promise<void>;
  clearResult: () => void;
  fetchHistory: () => Promise<void>;
}

export const useCheckerStore = create<CheckerStore>((set) => ({
  currentResult: null,
  isLoading: false,
  error: null,
  history: [],
  
  checkURL: async (url: string) => {
    set({ isLoading: true, error: null, currentResult: null });
    try {
      const response = await api.post('/check', { url });
      set({ currentResult: response.data, isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || error.message || 'An error occurred while checking the URL.',
        isLoading: false 
      });
    }
  },
  
  clearResult: () => set({ currentResult: null, error: null }),
  
  fetchHistory: async () => {
    try {
      const response = await api.get('/history');
      set({ history: response.data });
    } catch (error: any) {
      console.error('Failed to fetch history:', error);
    }
  }
}));
