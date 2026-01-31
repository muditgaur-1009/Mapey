'use client'

import { useState, useEffect } from 'react'
import { roadmapApi } from '@/lib/api'
import Link from 'next/link'
import { useUser, useClerk, UserButton } from '@clerk/nextjs'

export default function Header() {
  const { isLoaded, isSignedIn, user } = useUser()
  const { signOut } = useClerk()
  const [apiStatus, setApiStatus] = useState<'checking' | 'healthy' | 'unhealthy'>('checking')

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await roadmapApi.healthCheck()
        setApiStatus(health.status === 'healthy' ? 'healthy' : 'unhealthy')
      } catch (error) {
        setApiStatus('unhealthy')
        console.error('API health check failed:', error)
      }
    }

    checkHealth()
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="bg-black border-b border-red-900/60 shadow-sm">
      <div className="container mx-auto px-4 py-4 max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <h1 className="text-3xl md:text-xl font-bold font-orbitron tracking-widest text-red-500">
              MAPEY
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            {isLoaded && isSignedIn && user ? (
              <>
                <span className="text-xs sm:text-sm text-gray-300 max-w-[140px] sm:max-w-none truncate">
                  Signed in as <span className="font-semibold text-red-400">{user.fullName || user.primaryEmailAddress?.emailAddress}</span>
                </span>
                <button
                  onClick={() => signOut()}
                  className="px-3 py-1.5 rounded-full text-[11px] font-semibold border border-red-700 text-red-200
                             hover:bg-red-900/40 transition-colors"
                >
                  Log out
                </button>
                <UserButton afterSignOutUrl="/login" />
              </>
            ) : (
              <Link
                href="/login"
                className="px-4 py-1.5 rounded-full text-xs font-semibold border border-red-700 text-red-200
                           hover:bg-red-900/40 transition-colors"
              >
                Log in
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
