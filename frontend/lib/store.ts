import { create } from 'zustand'
import { RoadmapResponse } from '@/types/api'

interface RoadmapState {
  data: RoadmapResponse | null
  isLoading: boolean
  error: string | null
  progress: number
  currentStep: string
  setData: (data: RoadmapResponse | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  setProgress: (progress: number, step: string) => void
  reset: () => void
}

export const useRoadmapStore = create<RoadmapState>((set) => ({
  data: null,
  isLoading: false,
  error: null,
  progress: 0,
  currentStep: '',

  setData: (data) => set({ data, error: null, isLoading: false, progress: 100, currentStep: 'Complete!' }),
  setLoading: (isLoading) => set({ isLoading, progress: isLoading ? 0 : 100, currentStep: isLoading ? 'Initializing...' : '' }),
  setError: (error) => set({ error, isLoading: false, progress: 0, currentStep: '' }),
  setProgress: (progress, currentStep) => set({ progress, currentStep }),
  reset: () => set({ data: null, isLoading: false, error: null, progress: 0, currentStep: '' }),
}))

