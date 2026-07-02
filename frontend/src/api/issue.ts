import request from './request'

export interface Issue {
  id: number
  project_id: number
  title: string
  description: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'open' | 'in_progress' | 'resolved' | 'closed'
  reporter: string
  assignee: string
  created_at: string
  updated_at: string
}

export const issueApi = {
  list(params?: {
    page?: number
    pageSize?: number
    projectId?: number
    status?: string
    severity?: string
    keyword?: string
  }) {
    return request.get('/issues', { params })
  },

  detail(id: number) {
    return request.get(`/issues/${id}`)
  },

  create(data: Partial<Issue>) {
    return request.post('/issues', data)
  },

  update(id: number, data: Partial<Issue>) {
    return request.put(`/issues/${id}`, data)
  },

  delete(id: number) {
    return request.delete(`/issues/${id}`)
  },
}
