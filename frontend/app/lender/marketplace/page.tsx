'use client'

import { useState, useEffect } from 'react'
import { lenderAPI } from '@/lib/api'
import { SME } from '@/types'
import Link from 'next/link'

export default function Marketplace() {
  const [smes, setSmes] = useState<SME[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    industry: '',
    location: '',
    min_profit_score: 0
  })

  useEffect(() => {
    fetchSMEs()
  }, [filters])

  const fetchSMEs = async () => {
    try {
      const response = await lenderAPI.getMarketplace(filters)
      setSmes(response.data)
    } catch (error) {
      console.error('Failed to fetch SMEs:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            Verified SME Marketplace
          </h1>

          {/* Filters */}
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <select
                value={filters.industry}
                onChange={(e) => setFilters({...filters, industry: e.target.value})}
                className="border border-gray-300 rounded-md px-3 py-2"
              >
                <option value="">All Industries</option>
                <option value="retail">Retail</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="services">Services</option>
              </select>

              <select
                value={filters.location}
                onChange={(e) => setFilters({...filters, location: e.target.value})}
                className="border border-gray-300 rounded-md px-3 py-2"
              >
                <option value="">All Locations</option>
                <option value="lagos">Lagos</option>
                <option value="abuja">Abuja</option>
                <option value="kano">Kano</option>
              </select>

              <input
                type="number"
                placeholder="Min Profit Score"
                value={filters.min_profit_score}
                onChange={(e) => setFilters({...filters, min_profit_score: Number(e.target.value)})}
                className="border border-gray-300 rounded-md px-3 py-2"
              />
            </div>
          </div>

          {/* SME Grid */}
          {loading ? (
            <div className="text-center py-12">Loading verified SMEs...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {smes.map((sme) => (
                <Link key={sme.id} href={`/lender/marketplace/${sme.id}`}>
                  <div className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 cursor-pointer">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {sme.name}
                    </h3>
                    <p className="text-gray-600 mb-4">{sme.industry} • {sme.location}</p>
                    
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="text-sm text-gray-500">Pulse Score</span>
                        <div className="text-2xl font-bold text-green-600">
                          {sme.pulse_score}
                        </div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-500">Profit Score</span>
                        <div className="text-2xl font-bold text-blue-600">
                          {sme.profit_score}
                        </div>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}