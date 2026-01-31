import { create } from 'zustand'
import { RoadmapResponse } from '@/types/api'

interface RoadmapState {
  data: RoadmapResponse | null
  isLoading: boolean
  error: string | null
  setData: (data: RoadmapResponse | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  reset: () => void
}

export const useRoadmapStore = create<RoadmapState>((set) => ({
  data: null,
  isLoading: false,
  error: null,

  setData: (data) => set({ data, error: null, isLoading: false }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error, isLoading: false }),
  reset: () => set({ data: null, isLoading: false, error: null }),
}))

