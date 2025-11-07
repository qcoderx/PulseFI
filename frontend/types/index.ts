export interface SME {
  id: string
  name: string
  industry: string
  location: string
  pulse_score: number
  profit_score: number
  status: 'pending' | 'verified' | 'failed'
  description?: string
  founded_date?: string
}

export interface LenderUser {
  id: string
  name: string
  email: string
  company?: string
}

export interface SMEUser {
  id: string
  business_name: string
  email: string
  phone: string
  industry: string
  location: string
}

export interface AuthResponse {
  token: string
  user: LenderUser | SMEUser
  user_type: 'lender' | 'sme'
}