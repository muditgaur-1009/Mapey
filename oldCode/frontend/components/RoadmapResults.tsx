'use client'

import { useRoadmapStore } from '@/lib/store'
import ReactMarkdown from 'react-markdown'
import { FileText, BookOpen, Target, ExternalLink, Copy, Check } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'
import toast from 'react-hot-toast'

export default function RoadmapResults() {
  const { data, error, isLoading } = useRoadmapStore()
  const [copiedSection, setCopiedSection] = useState<string | null>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  const copyToClipboard = async (text: string, section: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedSection(section)
      toast.success('Copied to clipboard!')
      setTimeout(() => setCopiedSection(null), 2000)
    } catch (err) {
      toast.error('Failed to copy')
    }
  }

  // Auto-scroll to bottom when data loads
  // Scroll to top when new data loads
  useEffect(() => {
    if (data && scrollRef.current) {
      scrollRef.current.scrollTop = 0
    }
  }, [data])


  if (error) {
    return (
      <div className="h-screen flex items-center justify-center bg-black p-6">
        <div className="bg-black rounded-2xl shadow-2xl border border-red-800 p-12 max-w-lg w-full mx-4 text-center">
          <div className="w-24 h-24 mx-auto mb-8 bg-red-900/40 rounded-2xl flex items-center justify-center">
            <FileText className="w-12 h-12 text-red-500 dark:text-red-400" />
          </div>
          <h3 className="text-2xl font-bold text-white mb-4">
            Something went wrong
          </h3>
          <p className="text-gray-300 text-lg mb-8 max-w-md mx-auto leading-relaxed">
            {error}
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => window.location.reload()}
              className="px-8 py-3 bg-gradient-to-r from-primary-600 to-primary-800 text-white font-semibold rounded-xl hover:shadow-lg transition-all duration-300"
            >
              Try Again
            </button>
            <button
              className="px-8 py-3 bg-black border border-gray-700 text-gray-300 font-semibold rounded-xl hover:bg-red-950/40 transition-all duration-300"
              onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            >
              Back to Form
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (isLoading || !data) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black p-8">
      <div
        className="bg-black/80 backdrop-blur-md rounded-3xl p-16 text-center max-w-2xl w-full mx-auto
                   border border-red-600/40
                   shadow-[0_0_30px_rgba(239,68,68,0.25)]"
      >
        <div className="flex flex-col items-center space-y-6 mb-8">
          <div className="relative w-24 h-24 flex items-center justify-center">
            {isLoading ? (
              <div className="w-20 h-20 border-4 border-red-900 border-t-red-500 rounded-full animate-spin"></div>
            ) : (
              <Target className="w-24 h-24 text-red-500 drop-shadow-[0_0_12px_rgba(239,68,68,0.8)]" />
            )}
          </div>

          <div>
            <h3 className="text-3xl font-bold text-white mb-3 tracking-wide">
              {isLoading ? 'Generating Your Roadmap' : 'Ready to Generate'}
            </h3>

            <p className="text-xl text-gray-300 mb-2 font-semibold">
              {isLoading
                ? 'AI agents analyzing your profile...'
                : 'Fill in the form above and click "Generate Roadmap"'}
            </p>

            {isLoading && (
              <div className="flex space-x-2 text-sm text-gray-400 mt-3 justify-center">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
                <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            )}
          </div>
        </div>

        {!isLoading && (
          <div className="text-gray-400 text-lg leading-relaxed max-w-lg mx-auto">
            Our AI will create a personalized career roadmap based on:
            <ul className="mt-4 space-y-2 text-left list-disc list-inside marker:text-red-500">
              <li>Your target role and current skills</li>
              <li>Skill gap analysis</li>
              <li>Step-by-step learning curriculum</li>
              <li>Curated learning resources</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}


  // Data exists and not loading - show results
  const SectionCard = ({ 
    title, 
    icon: Icon, 
    content, 
    sectionKey 
  }: { 
    title: string
    icon: React.ElementType
    content: string
    sectionKey: string
  }) => (
    <div className="bg-black/90 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-8 border border-red-900/50 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 group">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl shadow-lg group-hover:scale-105 transition-all duration-300">
            <Icon className="w-7 h-7 text-white flex-shrink-0" />
          </div>
          <h3 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
            {title}
          </h3>
        </div>
        <button
          onClick={() => copyToClipboard(content, sectionKey)}
          className="p-4 bg-black/70 backdrop-blur-sm hover:bg-red-950/60 rounded-2xl shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105 group-hover-section"
          title="Copy to clipboard"
        >
          {copiedSection === sectionKey ? (
            <Check className="w-6 h-6 text-green-500" />
          ) : (
            <Copy className="w-6 h-6 text-gray-400 group-hover:text-white transition-colors" />
          )}
        </button>
      </div>
      <div className="prose dark:prose-invert max-w-none prose-headings:font-bold prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg prose-a:text-primary-400 prose-strong:font-semibold max-h-96 overflow-y-auto">
        <ReactMarkdown className="text-gray-200 whitespace-pre-wrap leading-relaxed scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
          {content}
        </ReactMarkdown>
      </div>
    </div>
  )

  return (
    <div className="h-screen overflow-hidden flex flex-col bg-black">
      {/* Fixed Header */}
      <div className="bg-black/90 backdrop-blur-md border-b border-red-900/60 px-8 py-6 sticky top-0 z-20 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-4xl font-black bg-gradient-to-r from-red-500 via-red-600 to-red-700 bg-clip-text text-transparent drop-shadow-lg">
              🎯 Your Career Roadmap
            </h2>
            <p className="text-gray-300 mt-1 font-medium">
              Personalized learning path generated for you
            </p>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-400 bg-black/70 px-4 py-2 rounded-full border border-gray-700">
            <Check className="w-4 h-4 text-green-500" />
            <span>Complete</span>
          </div>
        </div>
      </div>
      
      {/* Scrollable Content */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-8 pb-24 space-y-8 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent hover:scrollbar-thumb-gray-500"
      >
        <SectionCard title="📈 Career Roadmap" icon={Target} content={data.roadmap} sectionKey="roadmap" />
        <SectionCard title="🔍 Skill Gap Analysis" icon={Target} content={data.skill_gaps} sectionKey="skill_gaps" />
        <SectionCard title="📚 Learning Curriculum" icon={BookOpen} content={data.curriculum} sectionKey="curriculum" />
        
        {data.resources && (
          <div className="bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 rounded-2xl shadow-xl p-8 border border-emerald-200/50 dark:border-emerald-800/50">
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center space-x-4">
                <div className="p-4 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl shadow-lg">
                  <ExternalLink className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-3xl font-bold bg-gradient-to-r from-emerald-300 to-teal-300 bg-clip-text text-transparent">
                    🌐 Learning Resources
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">Curated links and materials</p>
                </div>
              </div>
              <button
                onClick={() => copyToClipboard(data.resources, 'resources')}
                className="p-4 bg-white/50 dark:bg-gray-700/50 backdrop-blur-sm hover:bg-white dark:hover:bg-gray-600 rounded-2xl shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105"
                title="Copy all resources"
              >
                {copiedSection === 'resources' ? <Check className="w-6 h-6 text-green-500" /> : <Copy className="w-6 h-6 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300" />}
              </button>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {data.resources.split('\n').map((item, idx) => {
                if (!item.trim()) return null
                const isUrl = item.startsWith('http://') || item.startsWith('https://')
                return (
                  <a
                    key={idx}
                    href={isUrl ? item : '#'}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group flex items-center space-x-4 p-6 bg-black/80 rounded-xl hover:bg-red-950/40 hover:shadow-lg hover:-translate-y-1 border border-gray-700/70 transition-all duration-300 overflow-hidden"
                  >
                    <div className="p-3 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-xl shadow-md group-hover:scale-110 transition-all duration-300 flex-shrink-0">
                      {isUrl ? <ExternalLink className="w-5 h-5 text-white" /> : <FileText className="w-5 h-5 text-white" />}
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="font-semibold text-gray-100 group-hover:text-emerald-300 truncate mb-1">
                        {item}
                      </p>
                      <p className="text-xs text-gray-500 group-hover:text-emerald-400">
                        {isUrl ? 'Open link' : 'Resource'}
                      </p>
                    </div>
                  </a>
                )
              })}
            </div>
          </div>
        )}

        {data.analysis && (
          <SectionCard title="💼 Role Analysis" icon={FileText} content={data.analysis} sectionKey="analysis" />
        )}
      </div>
    </div>
  )
}
