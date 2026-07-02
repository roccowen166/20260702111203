import request from './request'

export const reportApi = {
  exportIssues(params?: { projectId?: number; startDate?: string; endDate?: string }) {
    const query: Record<string, unknown> = {}
    if (params?.projectId) query.project_id = params.projectId
    if (params?.startDate) query.start_date = params.startDate
    if (params?.endDate) query.end_date = params.endDate
    return request.get('/reports/export-issues', {
      params: query,
      responseType: 'blob',
    })
  },

  exportTestCases(params?: { projectId?: number; status?: string }) {
    const query: Record<string, unknown> = {}
    if (params?.projectId) query.project_id = params.projectId
    if (params?.status) query.status = params.status
    return request.get('/reports/export-test-cases', {
      params: query,
      responseType: 'blob',
    })
  },

  exportAll(params?: { projectId?: number }) {
    const query: Record<string, unknown> = {}
    if (params?.projectId) query.project_id = params.projectId
    return request.get('/reports/export-all', {
      params: query,
      responseType: 'blob',
    })
  },
}
