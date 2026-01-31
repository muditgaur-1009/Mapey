import axios from 'axios'
import { RoadmapRequest, RoadmapResponse, ErrorResponse } from '../types/api'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
})

let backendToken: string | null = null

async function ensureBackendToken(): Promise<string> {
  if (backendToken) return backendToken

  const res = await fetch('/api/auth/backend-token')
  if (!res.ok) {
    throw new Error('You must be logged in to use the roadmap generator.')
  }
  const data = await res.json()
  backendToken = data.token
  if (!backendToken) {
    throw new Error('Failed to obtain backend token')
  }
  return backendToken
}

// Request interceptor for logging and Content-Type handling
apiClient.interceptors.request.use(
  async (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)

    // Attach backend JWT for protected endpoints
    if (config.url && config.url.startsWith('/roadmap/')) {
      const token = await ensureBackendToken()
      config.headers = config.headers || {}
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    // If FormData, let browser/axios set Content-Type automatically with boundary
    // Otherwise, set JSON content type for regular objects
    if (config.data instanceof FormData) {
      // Remove Content-Type header to let browser set it with boundary
      delete config.headers['Content-Type']
    } else if (config.data && typeof config.data === 'object' && !(config.data instanceof FormData)) {
      // Set JSON content type for regular objects
      config.headers['Content-Type'] = 'application/json'
    }
    
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const errorData: ErrorResponse = error.response.data
      console.error('[API] Response error:', errorData)
      throw new Error(errorData.detail || errorData.error || 'An error occurred')
    } else if (error.request) {
      console.error('[API] No response received:', error.request)
      throw new Error('No response from server. Please check if the API is running.')
    } else {
      console.error('[API] Error setting up request:', error.message)
      throw new Error('Request setup error: ' + error.message)
    }
  }
)

export const roadmapApi = {
  /**
   * Generate roadmap from file upload
   */
  async generateFromFile(
    topic: string,
    resumeFile: File,
    jd?: string
  ): Promise<RoadmapResponse> {
    const formData = new FormData()
    formData.append('topic', topic)
    formData.append('resume_file', resumeFile)
    if (jd && jd.trim()) {
      formData.append('jd', jd.trim())
    }

    const response = await apiClient.post<RoadmapResponse>(
      '/roadmap/generate',
      formData,
      {
        timeout: 300000, // 5 minutes timeout for long-running requests
      }
    )

    return response.data
  },

  /**
   * Generate roadmap from text input
   */
  async generateFromText(request: RoadmapRequest): Promise<RoadmapResponse> {
    const response = await apiClient.post<RoadmapResponse>(
      '/roadmap/generate-from-text',
      request,
      {
        timeout: 300000, // 5 minutes timeout
      }
    )

    return response.data
  },

  /**
   * Generate roadmap with streaming progress updates
   */
  async generateFromTextStream(
    request: RoadmapRequest,
    onProgress: (data: { progress: number; step: string; status: string }) => void
  ): Promise<RoadmapResponse> {
    const token = await ensureBackendToken()
    
    const response = await fetch(`${API_URL}/api/v1/roadmap/generate-from-text-stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('No response body')
    }

    const decoder = new TextDecoder()
    let buffer = ''
    let finalResult: RoadmapResponse | null = null

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.trim() === '' || !line.startsWith('data:')) continue
          
          const data = line.replace(/^data:\s*/, '')
          try {
            const parsed = JSON.parse(data)
            
            if (parsed.status === 'complete' && parsed.result) {
              finalResult = parsed.result
            } else if (parsed.status === 'error') {
              throw new Error(parsed.error || 'Unknown error occurred')
            } else {
              onProgress({
                progress: parsed.progress || 0,
                step: parsed.step || 'Processing...',
                status: parsed.status || 'processing'
              })
            }
          } catch (e) {
            console.warn('Failed to parse SSE data:', data)
          }
        }
      }
    } finally {
      reader.releaseLock()
    }

    if (!finalResult) {
      throw new Error('No result received from server')
    }

    return finalResult
  },

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string; version: string; service: string }> {
    const response = await apiClient.get('/health/')
    return response.data
  },
}

export default apiClient
