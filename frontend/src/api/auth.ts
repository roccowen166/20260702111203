import request from './request'

export interface LoginParams {
  email: string
  password: string
}

export interface LoginResult {
  access_token: string
  token_type: string
  user: {
    id: number
    email: string
    full_name: string
    role: 'admin' | 'user'
  }
}

export interface UserCreateParams {
  email: string
  password: string
  full_name: string
  role?: 'admin' | 'user'
}

export const authApi = {
  login(data: LoginParams) {
    return request.post<LoginResult>('/auth/login', data)
  },

  register(data: UserCreateParams) {
    return request.post('/auth/register', data)
  },

  me() {
    return request.get('/auth/me')
  },
}
