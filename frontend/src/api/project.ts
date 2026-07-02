import request from './request'

export interface Project {
  id: number
  name: string
  description: string
  status: string
  created_at: string
  updated_at: string
}

export interface ProjectFile {
  id: number
  project_id: number
  filename: string
  file_type: string
  file_url: string
  file_size: number
  uploaded_at: string
}

export const projectApi = {
  list(params?: { page?: number; pageSize?: number; keyword?: string }) {
    return request.get('/projects', { params })
  },

  detail(id: number) {
    return request.get(`/projects/${id}`)
  },

  create(data: Partial<Project>) {
    return request.post('/projects', data)
  },

  update(id: number, data: Partial<Project>) {
    return request.put(`/projects/${id}`, data)
  },

  delete(id: number) {
    return request.delete(`/projects/${id}`)
  },

  files(projectId: number) {
    return request.get(`/projects/${projectId}/files`)
  },

  uploadFile(projectId: number, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post(`/projects/${projectId}/files`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  deleteFile(projectId: number, fileId: number) {
    return request.delete(`/projects/${projectId}/files/${fileId}`)
  },
}
