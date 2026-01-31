import { clerkMiddleware } from '@clerk/nextjs/server'
import { NextResponse } from 'next/server'

export default clerkMiddleware()

// Protect all routes by default, but you could narrow this if needed.
export const config = {
  matcher: [
    // API routes that require auth
    '/api/auth/backend-token',
    '/api/((?!_next/|public/).*)',
    // App routes (you can relax this later if you want some fully public)
    '/((?!_next/|public/|favicon.ico).*)',
  ],
}
