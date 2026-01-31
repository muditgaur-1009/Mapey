import NextAuth, { NextAuthOptions } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import GithubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'

export const authOptions: NextAuthOptions = {
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: 'jwt',
  },
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
    }),
    GithubProvider({
      clientId: process.env.GITHUB_ID || '',
      clientSecret: process.env.GITHUB_SECRET || '',
    }),
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials.password) {
          return null
        }

        const demoEmail = process.env.DEMO_USER_EMAIL
        const demoPassword = process.env.DEMO_USER_PASSWORD

        if (demoEmail && demoPassword) {
          if (
            credentials.email === demoEmail &&
            credentials.password === demoPassword
          ) {
            return {
              id: 'demo-user',
              name: 'Demo User',
              email: demoEmail,
            }
          }
          return null
        }

        // Fallback: accept any non-empty credentials (development only)
        if (process.env.NODE_ENV !== 'production') {
          return {
            id: credentials.email,
            name: credentials.email.split('@')[0],
            email: credentials.email,
          }
        }

        return null
      },
    }),
  ],
  pages: {
    signIn: '/login',
  },
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }
