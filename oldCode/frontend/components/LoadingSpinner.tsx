'use client'

export default function LoadingSpinner() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-12">
      <div className="flex flex-col items-center justify-center space-y-4">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-primary-200 dark:border-primary-800 border-t-primary-600 dark:border-t-primary-400 rounded-full animate-spin"></div>
        </div>
        <div className="text-center">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Generating Your Roadmap
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            This may take a few moments. Our AI agents are working hard to create your personalized career roadmap...
          </p>
        </div>
        <div className="flex space-x-2 mt-4">
          <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  )
}
