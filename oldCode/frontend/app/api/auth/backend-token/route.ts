import { NextResponse } from 'next/server'
import { auth } from '@clerk/nextjs/server'
import jwt from 'jsonwebtoken'

export async function GET() {
  const { userId, sessionClaims } = auth()

  if (!userId) {
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
