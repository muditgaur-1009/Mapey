import type { Metadata } from 'next'
import { Inter, Orbitron } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'
import { ClerkProvider } from '@clerk/nextjs'
import { dark } from '@clerk/themes'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const orbitron = Orbitron({
  subsets: ['latin'],
  weight: ['400', '600', '700', '900'],
  variable: '--font-orbitron',
})

export const metadata: Metadata = {
  title: 'Mapey - AI Career Roadmap Generator',
  description: 'Generate personalized career roadmaps powered by AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark,
        variables: {
          colorBackground: '#000000',
          colorPrimary: '#ef4444',
          colorText: '#f9fafb',
          colorTextSecondary: '#9ca3af',
          borderRadius: '0.75rem',
          fontSize: '0.9rem',
        },
        elements: {
          card: 'bg-black/90 border border-red-900/60 shadow-2xl',
          headerTitle: 'text-white font-orbitron tracking-[0.2em]',
          headerSubtitle: 'text-gray-400',
          formFieldLabel: 'text-gray-300',
          formFieldInput: 'bg-black/60 border border-gray-700 text-white',
          formButtonPrimary:
            'bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl',
          footer: 'text-gray-500',
        },
      }}
    >
      <html lang="en" className={`${inter.variable} ${orbitron.variable}`}>
        <body className="font-sans">
          {children}

          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 5000,
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </body>
      </html>
    </ClerkProvider>
  )
}
