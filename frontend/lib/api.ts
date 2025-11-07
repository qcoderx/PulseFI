import axios from 'axios'
import Cookies from 'js-cookie'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = Cookies.get('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  loginLender: (email: string, password: string) =>
    api.post('/auth/login', { email, password, user_type: 'lender' }),
  
  registerLender: (data: any) =>
    api.post('/auth/lender/register', data),
  
  loginSME: (email: string, password: string) =>
    api.post('/auth/login', { email, password, user_type: 'sme' }),
  
  registerSME: (data: any) =>
    api.post('/auth/sme/register', data),
}

export const lenderAPI = {
  getMarketplace: (filters?: any) =>
    api.get('/lender/marketplace', { params: filters }),
  
  getSMEDetails: (smeId: string) =>
    api.get(`/lender/marketplace/${smeId}`),
}

export const smeAPI = {
  updateProfile: (data: any) =>
    api.post('/sme/profile', data),
  
  uploadCAC: (file: File) => {
    const formData = new FormData()
    formData.append('cac_file', file)
    return api.post('/sme/upload/cac', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  uploadVideo: (file: Blob) => {
    const formData = new FormData()
    formData.append('video_file', file)
    return api.post('/sme/upload/video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  connectMono: (token: string) =>
    api.post('/sme/mono/connect', { mono_token: token }),
  
  getDashboard: () =>
    api.get('/sme/dashboard'),
}

export default api