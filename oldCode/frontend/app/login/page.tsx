'use client'

import { useSearchParams } from 'next/navigation'
import { SignIn } from '@clerk/nextjs'
import { Github } from 'lucide-react'

export default function LoginPage() {
  // const router = useRouter()
  const searchParams = useSearchParams()
  const callbackUrl = searchParams.get('callbackUrl') || '/'

  return (
    <main className="min-h-screen bg-black flex items-center justify-center px-4">
      <div className="max-w-4xl w-full grid md:grid-cols-2 gap-10 items-center">
        <div className="space-y-6 text-center md:text-left">
          <h1 className="font-orbitron text-5xl md:text-6xl font-extrabold tracking-[0.2em]
               bg-gradient-to-r from-indigo-500 via-red-500 to-pink-500
               text-transparent bg-clip-text drop-shadow-sm">
            MAPEY
          </h1>
          <p className="text-xl text-gray-300 font-semibold">
            Sign in to access your AI-powered career roadmaps.
          </p>
          <p className="text-sm text-gray-500 max-w-md">
            Use your Google, GitHub, or a demo email and password to log in.
          </p>
        </div>

        <div className="bg-black/80 border border-red-900/60 rounded-2xl shadow-2xl p-8 space-y-6">
          <h2 className="text-2xl font-bold text-white mb-2">Welcome back</h2>
          <p className="text-sm text-gray-400 mb-4">
            Sign in with Clerk to access the app.
          </p>
          <div className="space-y-6">
            <SignIn
              routing="path"
              path="/login"
              signUpUrl="/login"
              fallbackRedirectUrl={callbackUrl}
            />
          </div>
        </div>
      </div>
    </main>
  )
}
