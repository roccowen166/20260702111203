import request from './request'

export interface TestCaseStep {
  step_no: number
  action: string
  expected_result: string
}

export interface TestCase {
  id: number
  project_id: number
  title: string
  description: string
  preconditions: string
  steps: TestCaseStep[]
  priority: 'low' | 'medium' | 'high'
  status: 'draft' | 'active' | 'deprecated'
  created_by: number | null
  created_by_name: string
  created_at: string
  updated_at: string
}

export const testCaseApi = {
  list(params?: {
    page?: number
    pageSize?: number
    projectId?: number
    status?: string
    priority?: string
    keyword?: string
  }) {
    return request.get('/test-cases', { params })
  },

  detail(id: number) {
    return request.get(`/test-cases/${id}`)
  },

  create(data: Partial<TestCase>) {
    return request.post('/test-cases', data)
  },

  update(id: number, data: Partial<TestCase>) {
    return request.put(`/test-cases/${id}`, data)
  },

  delete(id: number) {
    return request.delete(`/test-cases/${id}`)
  },
}
