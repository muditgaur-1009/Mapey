import { NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs/server'
import jwt from 'jsonwebtoken'

export async function GET() {
  const { userId, sessionClaims } = auth()

  // If Clerk isn't configured and we're in local development, provide a dev token
  // to make local testing easier. This is intentionally limited to NODE_ENV=development.
  if (!userId) {
    const isClerkConfigured = Boolean(process.env.CLERK_SECRET_KEY || process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY)
    if (process.env.NODE_ENV === 'development' && !isClerkConfigured) {
      const secret = process.env.BACKEND_JWT_SECRET || process.env.NEXTAUTH_SECRET

      if (!secret) {
        return NextResponse.json(
          { error: 'Backend JWT secret not configured' },
          { status: 500 }
        )
      }

      const email = process.env.DEV_USER_EMAIL || process.env.DEMO_USER_EMAIL || 'dev@example.com'
      const name = process.env.DEV_USER_NAME || 'Dev User'
      const identifier = 'dev_user'

      const token = jwt.sign(
        {
          sub: identifier,
          email,
          name,
        },
        secret,
        { expiresIn: '1h' }
      )

      return NextResponse.json({ token })
    }

    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const secret = process.env.BACKEND_JWT_SECRET || process.env.NEXTAUTH_SECRET

  if (!secret) {
    return NextResponse.json(
      { error: 'Backend JWT secret not configured' },
      { status: 500 }
    )
  }

  const identifier = userId

  const token = jwt.sign(
    {
      sub: identifier,
      // Include basic Clerk session data if available
      email: (sessionClaims as any)?.email,
      name: (sessionClaims as any)?.name,
    },
    secret,
    { expiresIn: '1h' }
  )

  return NextResponse.json({ token })
}
