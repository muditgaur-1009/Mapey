'use client'

import { useState, useEffect } from 'react'
import { roadmapApi } from '@/lib/api'
import Link from 'next/link'
import { useUser, useClerk, UserButton } from '@clerk/nextjs'

export default function Header() {
  // Fallback when Clerk not configured in local development (use a single publishable key)
  const isClerkEnabled = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY)
  const { isLoaded: clerkLoaded, isSignedIn: clerkSignedIn, user: clerkUser } = useUser() as any
  const { signOut: clerkSignOut } = useClerk?.() as any || { signOut: () => {} }

  const [authTimedOut, setAuthTimedOut] = useState(false)
  useEffect(() => {
    if (!isClerkEnabled) return
    if (clerkLoaded) return
    const t = setTimeout(() => setAuthTimedOut(true), 3000)
    return () => clearTimeout(t)
  }, [isClerkEnabled, clerkLoaded])

  const isLoaded = isClerkEnabled ? (clerkLoaded || authTimedOut) : true
  const devSignedIn = (typeof window !== 'undefined' && localStorage.getItem('MAPEY_DEV_SIGNED_IN') === 'true')
  const isSignedIn = isClerkEnabled ? (clerkSignedIn || (authTimedOut && devSignedIn)) : (process.env.NEXT_PUBLIC_DEV_SIGNED_IN === 'true')
  const user = isClerkEnabled ? clerkUser : { fullName: process.env.NEXT_PUBLIC_DEV_USER_NAME || process.env.DEMO_USER_EMAIL || 'Dev User', primaryEmailAddress: { emailAddress: process.env.DEMO_USER_EMAIL || 'dev@example.com' } }

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
                  onClick={() => {
                    if (isClerkEnabled) {
                      clerkSignOut()
                    } else {
                      // In dev fallback, just redirect to /login
                      window.location.href = '/login'
                    }
                  }}
                  className="px-3 py-1.5 rounded-full text-[11px] font-semibold border border-red-700 text-red-200
                             hover:bg-red-900/40 transition-colors"
                >
                  Log out
                </button>
                {isClerkEnabled ? <UserButton afterSignOutUrl="/login" /> : null}
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
