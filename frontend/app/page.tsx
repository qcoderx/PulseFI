import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            PulseFi
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            The Trust Engine for SME Lending - Solving the Billion-Naira Trust Gap
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/auth/lender/login"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
            >
              I'm a Lender
            </Link>
            <Link 
              href="/auth/sme/login"
              className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
            >
              I'm an SME
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}