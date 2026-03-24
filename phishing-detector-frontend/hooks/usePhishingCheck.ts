import { useState } from 'react';
import { useCheckerStore } from '../store/useCheckerStore';

export function usePhishingCheck() {
  const { checkURL, isLoading, error, currentResult, clearResult } = useCheckerStore();
  const [localError, setLocalError] = useState<string | null>(null);

  const handleCheck = async (url: string) => {
    setLocalError(null);
    try {
      await checkURL(url);
    } catch (err: any) {
      setLocalError(err.message || 'An unexpected error occurred during check.');
    }
  };

  return {
    handleCheck,
    isLoading,
    error: error || localError,
    result: currentResult,
    clearResult,
  };
}
