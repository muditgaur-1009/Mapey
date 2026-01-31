'use client'

import { useState, useEffect } from 'react'
import { useUser, SignInButton } from '@clerk/nextjs'
import { useRoadmapStore } from '@/lib/store'
import RoadmapForm from '@/components/RoadmapForm'
import RoadmapResults from '@/components/RoadmapResults'
import Header from '@/components/Header'

export default function Home() {
  const { isLoading } = useRoadmapStore()

  // Use Clerk when configured; otherwise synthesize loaded state in dev so UI doesn't hang.
  const isClerkEnabled = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY)
  const { isLoaded: clerkLoaded, isSignedIn: clerkSignedIn } = useUser() as any

  const [authTimedOut, setAuthTimedOut] = useState(false)

  useEffect(() => {
    if (!isClerkEnabled) return
    if (clerkLoaded) return

    const t = setTimeout(() => {
      console.warn('Clerk did not finish loading within expected time - enabling dev fallback for UI.')
      setAuthTimedOut(true)
    }, 3000)

    return () => clearTimeout(t)
  }, [isClerkEnabled, clerkLoaded])

  const isLoaded = isClerkEnabled ? (clerkLoaded || authTimedOut) : true
  // Allow explicit runtime dev override via localStorage (set by the fallback button)
  const devSignedIn = (typeof window !== 'undefined' && localStorage.getItem('MAPEY_DEV_SIGNED_IN') === 'true')
  const isSignedIn = isClerkEnabled ? (clerkSignedIn || authTimedOut && devSignedIn) : (process.env.NEXT_PUBLIC_DEV_SIGNED_IN === 'true')

  if (!isLoaded) {
    return (
      <main className="min-h-screen bg-black flex items-center justify-center text-white">
        <p className="text-gray-300">Checking authentication...</p>
      </main>
    )
  }

  // If we timed out waiting for Clerk to load, show a helpful fallback and allow continuing in dev mode
  if (isClerkEnabled && authTimedOut && !clerkLoaded) {
    return (
      <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-4">
        <Header />
        <div className="max-w-xl text-center space-y-6 mt-12">
          <h2 className="text-xl font-semibold">Clerk is taking too long to initialize</h2>
          <p className="text-sm text-gray-300">This can happen if Clerk is not configured correctly. Check <code className="bg-gray-800 px-2 py-0.5 rounded">.env.local</code> and ensure <code className="bg-gray-800 px-2 py-0.5 rounded">NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY</code> is set (and add <code className="bg-gray-800 px-2 py-0.5 rounded">CLERK_SECRET_KEY</code> to the backend for server operations).</p>
          <div className="flex items-center gap-3 justify-center">
            <button
              onClick={() => {
                try {
                  localStorage.setItem('MAPEY_DEV_SIGNED_IN', 'true')
                } catch (e) {}
                // Reload to pick up the dev-signed-in flag
                window.location.reload()
              }}
              className="px-6 py-2 rounded-full bg-red-600 text-white font-semibold"
            >
              Continue in dev mode
            </button>
            <a href="/login" className="px-6 py-2 rounded-full border border-gray-700 text-gray-200">Open login page</a>
          </div>
        </div>
      </main>
    )
  }

  if (!isSignedIn) {
    return (
      <main className="min-h-screen bg-black text-white flex flex-col">
        <Header />
        <div className="flex-1 flex items-center justify-center px-4">
          <div className="max-w-xl text-center space-y-6">
            <h1 className="font-orbitron text-4xl md:text-5xl font-extrabold tracking-[0.2em]
                 bg-gradient-to-r from-indigo-500 via-red-500 to-pink-500
                 text-transparent bg-clip-text drop-shadow-sm">
              MAPEY
            </h1>
            <p className="text-lg text-gray-300 font-semibold">
              Sign in to generate your personalized AI career roadmap.
            </p>
            <p className="text-sm text-gray-500">
              Sign in with your Clerk account to access the roadmap generator.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center mt-4">
              {isClerkEnabled ? (
                <SignInButton mode="modal">
                  <button
                    className="px-6 py-2.5 rounded-full bg-gradient-to-r from-red-500 via-red-600 to-red-700
                               text-sm font-semibold shadow-lg hover:from-red-600 hover:to-red-800"
                  >
                    Log in to continue
                  </button>
                </SignInButton>
              ) : (
                <a
                  href="/login"
                  className="px-6 py-2.5 rounded-full bg-gradient-to-r from-red-500 via-red-600 to-red-700
                             text-sm font-semibold shadow-lg hover:from-red-600 hover:to-red-800"
                >
                  Log in to continue
                </a>
              )}
            </div>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <Header />
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="text-center mb-8">
          <h1 className="font-orbitron text-5xl md:text-6xl font-extrabold tracking-[0.2em]
               bg-gradient-to-r from-indigo-500 via-red-500 to-pink-500
               text-transparent bg-clip-text drop-shadow-sm">
            MAPEY
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-2">
            AI-Powered Career Roadmap Generator
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Upload your resume, specify your target role, and get a personalized learning roadmap
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <RoadmapForm />
          </div>
          
          <div className="lg:col-span-2">
            <RoadmapResults />
          </div>
        </div>
      </div>
    </main>
  )
}
