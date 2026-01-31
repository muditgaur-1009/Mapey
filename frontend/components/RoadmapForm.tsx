'use client'

import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { roadmapApi } from '@/lib/api'
import { useRoadmapStore } from '@/lib/store'
import toast from 'react-hot-toast'
import { Upload, FileText, X, Send } from 'lucide-react'
import clsx from 'clsx'

export default function RoadmapForm() {
  const [topic, setTopic] = useState('')
  const [jd, setJd] = useState('')
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [resumeText, setResumeText] = useState('')
  const [useTextInput, setUseTextInput] = useState(false)
  const [localLoading, setLocalLoading] = useState(false)

  const { isLoading, setLoading, setError, setData, setProgress } = useRoadmapStore()
  const loading = isLoading || localLoading

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setResumeFile(acceptedFiles[0])
        setUseTextInput(false)
        toast.success('File uploaded successfully')
      }
    },
    onDropRejected: () => {
      toast.error('Invalid file type. Please upload PDF or TXT files only.')
    },
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // ✅ VALIDATION FIRST (no loading yet)

    if (!topic.trim()) {
      toast.error('Please enter a target role')
      return
    }

    if (!resumeFile && !resumeText.trim()) {
      toast.error('Please upload a resume file or enter resume text')
      return
    }

    // ✅ NOW start loading (both global store + local fallback)
    setLocalLoading(true)
    setLoading(true)
    setError(null)
    setProgress(0, 'Initializing...')

    try {
      let response

      // Use streaming for text input to show progress
      if (useTextInput && resumeText.trim()) {
        response = await roadmapApi.generateFromTextStream(
          {
            topic: topic.trim(),
            resume: resumeText.trim(),
            jd: jd.trim() || undefined,
          },
          (progressData) => {
            setProgress(progressData.progress, progressData.step)
          }
        )
      } else if (resumeFile && !useTextInput) {
        // For file upload, use streaming too but read file first
        const fileText = await resumeFile.text()
        response = await roadmapApi.generateFromTextStream(
          {
            topic: topic.trim(),
            resume: fileText,
            jd: jd.trim() || undefined,
          },
          (progressData) => {
            setProgress(progressData.progress, progressData.step)
          }
        )
      } else {
        if (!resumeText.trim()) {
          setError('Please enter resume text')
          toast.error('Please enter resume text')
          return
        }

        response = await roadmapApi.generateFromText({
          topic: topic.trim(),
          resume: resumeText.trim(),
          jd: jd.trim() || undefined,
        })
      }

      setData(response)
      setProgress(100, 'Complete!')
      toast.success('Roadmap generated successfully!')
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to generate roadmap'
      setError(errorMessage)
      toast.error(errorMessage)
      setProgress(0, '')
    } finally {
      // ensure both local and global loading flags are cleared
      setLocalLoading(false)
      setLoading(false)
    }
  }

  return (
    <div className="bg-black border border-red-600/40 rounded-xl p-6 max-w-2xl mx-auto
shadow-[0_0_20px_rgba(239,68,68,0.15)]">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center space-x-2">
        <FileText className="w-7 h-7 text-primary-600" />
        <span>Input Details</span>
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Target Role */}
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Target Role *
          </label>
          <input
            type="text"
            id="topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., ML Engineer, Full Stack Developer, Data Scientist"
            disabled={loading}
            className="w-full px-4 py-3 rounded-xl 
                      bg-black text-white
                      border border-gray-700
                      placeholder-gray-500
                      focus:border-red-500 focus:ring-1 focus:ring-red-500
                      transition-all duration-200
                      disabled:opacity-50 disabled:cursor-not-allowed"
          />



        </div>

        {/* Job Description */}
        <div>
          <label htmlFor="jd" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Job Description (Optional)
          </label>
          <textarea
            id="jd"
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            placeholder="Paste job description here to get more targeted roadmap..."
            rows={4}
            disabled={loading}
            className="w-full px-4 py-3 rounded-xl bg-black text-white
                      border border-gray-700
                      placeholder-gray-500 resize-none
                      focus:border-red-500 focus:ring-1 focus:ring-red-500
                      transition-all duration-200
                      disabled:opacity-50 disabled:cursor-not-allowed"
          />

        </div>

        {/* Resume Input Toggle */}
        <div className="flex items-center space-x-4 mb-4 p-4 bg-gray-50 dark:bg-gray-900/50 rounded-xl">
          <button
            type="button"
            onClick={() => setUseTextInput(false)}
            disabled={loading}
            className={clsx(
              'flex-1 px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2',
              !useTextInput
                ? 'bg-primary-600 text-white shadow-md hover:shadow-lg hover:bg-primary-700 active:scale-95'
                : 'bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600'
            )}
          >
            <Upload className="w-4 h-4" />
            <span>Upload File</span>
          </button>

          <button
          type="button"
          onClick={() => {
            setUseTextInput(true)
            setResumeFile(null)
          }}
          disabled={loading}
          className={clsx(
            'flex-1 px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center justify-center space-x-2',
            useTextInput
              ? 'bg-red-600 text-white shadow-[0_0_15px_rgba(239,68,68,0.5)] hover:bg-red-700 active:scale-95'
              : 'bg-black border border-red-600/40 text-gray-300 hover:bg-red-600/10'
          )}
        >
          <FileText className="w-4 h-4" />
          <span>Enter Text</span>
        </button>
        </div>

        {/* File Upload */}
        {!useTextInput && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Resume (PDF or TXT) *
            </label>
            <div
              {...getRootProps()}
              className={clsx(
                'border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all duration-300 group hover:shadow-md',
                (isDragActive || resumeFile) && !loading
                  ? 'border-primary-500 bg-primary-50/50 dark:bg-primary-900/20 shadow-lg ring-2 ring-primary-200 dark:ring-primary-800'
                  : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500 hover:bg-gray-50 dark:hover:bg-gray-800/50'
              )}
            >
              <input {...getInputProps()} />
              {resumeFile ? (
                <div className="flex flex-col sm:flex-row items-center justify-center space-y-2 sm:space-y-0 sm:space-x-4 text-primary-600 dark:text-primary-400">
                  <div className="flex items-center space-x-3 p-3 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
                    <FileText className="w-6 h-6" />
                    <span className="font-semibold truncate max-w-xs">{resumeFile.name}</span>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation()
                      setResumeFile(null)
                    }}
                    disabled={loading}
                    className="p-2 text-red-500 hover:text-red-700 hover:bg-red-100 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              ) : (
                <div className="space-y-3">
                  <Upload className="w-16 h-16 mx-auto text-gray-400 group-hover:text-primary-500 transition-colors" />
                  <div>
                    <p className="text-lg font-semibold text-gray-700 dark:text-gray-300 group-hover:text-primary-600">
                      {isDragActive ? 'Drop the file here...' : 'Drag & drop resume file'}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">or click to select</p>
                  </div>
                  <p className="text-xs text-gray-400 dark:text-gray-500 font-medium">
                    Supports PDF and TXT files only
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Text Input */}
        {useTextInput && (
          <div>
            <label htmlFor="resume" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Resume Text *
            </label>
            <textarea
              id="resume"
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder={`Paste your complete resume content here... Include education, work experience, skills, projects, certifications etc.`}
              rows={10}
              disabled={loading}
              className="w-full px-4 py-3 rounded-xl bg-black text-white
                        border border-gray-700
                        placeholder-gray-500 resize-vertical
                        font-mono text-sm leading-relaxed
                        focus:border-red-500 focus:ring-1 focus:ring-red-500
                        transition-all duration-200
                        disabled:opacity-50 disabled:cursor-not-allowed"
            />

          </div>
        )}

        {/* Submit Button */}
        <button
        type="submit"
        disabled={loading}
        className={clsx(
          'w-full font-bold py-4 px-8 rounded-xl transition-all duration-300 flex items-center justify-center space-x-3 shadow-[0_0_20px_rgba(239,68,68,0.35)] active:scale-95 disabled:cursor-not-allowed disabled:opacity-70',
          loading
            ? 'bg-gradient-to-r from-red-700 to-red-500 text-white'
            : 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white hover:shadow-[0_0_25px_rgba(239,68,68,0.45)]'
        )}
      >
        {loading ? (
          <>
            <div className="relative w-6 h-6 flex items-center justify-center">
              <div
                className="w-6 h-6 rounded-full animate-spin"
                style={{
                  border: '3px solid rgba(255, 255, 255, 0.2)',
                  borderTop: '3px solid #ff3c3c',
                  boxSizing: 'border-box',
                }}
              />
            </div>
            <span className="tracking-wide text-lg font-bold text-white">
              Generating Your Roadmap...
            </span>
          </>
        ) : (
          <>
            <Send className="w-6 h-6 text-white drop-shadow-[0_0_6px_rgba(239,68,68,0.7)]" />
            <span className="tracking-wide text-lg font-bold text-white">
              Generate Roadmap
            </span>
          </>
        )}
      </button>

      </form>
    </div>
  )
}
