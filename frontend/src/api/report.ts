import request from './request'

export const reportApi = {
  exportIssues(params?: { projectId?: number; startDate?: string; endDate?: string }) {
    return request.get('/reports/export-issues', {
      params,
      responseType: 'blob',
    })
  },

  exportTestCases(params?: { projectId?: number; status?: string }) {
    return request.get('/reports/export-test-cases', {
      params,
      responseType: 'blob',
    })
  },

  exportAll(params?: { projectId?: number }) {
    return request.get('/reports/export-all', {
      params,
      responseType: 'blob',
    })
  },
}
