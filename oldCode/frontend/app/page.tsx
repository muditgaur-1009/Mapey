'use client'

import { useState } from 'react'
import { useUser, SignInButton } from '@clerk/nextjs'
import { useRoadmapStore } from '@/lib/store'
import RoadmapForm from '@/components/RoadmapForm'
import RoadmapResults from '@/components/RoadmapResults'
import Header from '@/components/Header'

export default function Home() {
  const { isLoading } = useRoadmapStore()
  const { isLoaded, isSignedIn } = useUser()

  if (!isLoaded) {
    return (
      <main className="min-h-screen bg-black flex items-center justify-center text-white">
        <p className="text-gray-300">Checking authentication...</p>
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
              <SignInButton mode="modal">
                <button
                  className="px-6 py-2.5 rounded-full bg-gradient-to-r from-red-500 via-red-600 to-red-700
                             text-sm font-semibold shadow-lg hover:from-red-600 hover:to-red-800"
                >
                  Log in to continue
                </button>
              </SignInButton>
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
