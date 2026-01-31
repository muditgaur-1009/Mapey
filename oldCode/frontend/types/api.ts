export interface RoadmapRequest {
  topic: string
  resume: string
  jd?: string
}

export interface RoadmapResponse {
  roadmap: string
  skill_gaps: string
  curriculum: string
  resources: string
  analysis?: string
  rag_context?: string
}

export interface ErrorResponse {
  error: string
  detail?: string
  code?: string
}

export interface HealthResponse {
  status: 'healthy' | 'unhealthy'
  version: string
  service: string
}
