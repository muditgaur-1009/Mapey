'use client'

import { useEffect, useState } from 'react'
import { Loader2 } from 'lucide-react'
import clsx from 'clsx'

interface ProgressBarProps {
  progress: number
  currentStep: string
  className?: string
}

export default function ProgressBar({ progress, currentStep, className }: ProgressBarProps) {
  const [displayProgress, setDisplayProgress] = useState(0)
  
  // Smooth animation for progress
  useEffect(() => {
    const timer = setTimeout(() => {
      setDisplayProgress(progress)
    }, 100)
    return () => clearTimeout(timer)
  }, [progress])

  return (
    <div className={clsx("w-full space-y-3", className)}>
      {/* Progress Bar */}
      <div className="relative w-full h-3 bg-gray-800 rounded-full overflow-hidden border border-gray-700">
        <div
          className={clsx(
            "h-full rounded-full transition-all duration-500 ease-out",
            "bg-gradient-to-r from-red-600 via-red-500 to-red-400",
            "shadow-[0_0_15px_rgba(239,68,68,0.5)]"
          )}
          style={{ width: `${displayProgress}%` }}
        >
          {/* Animated shine effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
        </div>
        
        {/* Percentage Label */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xs font-bold text-white drop-shadow-lg">
            {Math.round(displayProgress)}%
          </span>
        </div>
      </div>

      {/* Current Step Description */}
      <div className="flex items-center space-x-2 text-sm">
        <Loader2 className="w-4 h-4 text-red-500 animate-spin" />
        <span className="text-gray-300 font-medium">{currentStep}</span>
      </div>

      {/* Stage Indicators */}
      <div className="grid grid-cols-6 gap-2 mt-4">
        {[
          { name: 'Analyzing', threshold: 10 },
          { name: 'Skill Gaps', threshold: 30 },
          { name: 'Curriculum', threshold: 50 },
          { name: 'Resources', threshold: 70 },
          { name: 'Context', threshold: 65 },
          { name: 'Finalizing', threshold: 85 }
        ].map((stage, idx) => {
          const isActive = displayProgress >= stage.threshold
          const isComplete = displayProgress > stage.threshold + 15
          
          return (
            <div key={idx} className="flex flex-col items-center space-y-1">
              <div
                className={clsx(
                  "w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300",
                  isComplete && "bg-red-600 text-white shadow-[0_0_10px_rgba(239,68,68,0.5)]",
                  isActive && !isComplete && "bg-red-500/50 text-red-200 animate-pulse",
                  !isActive && "bg-gray-800 text-gray-600 border border-gray-700"
                )}
              >
                {isComplete ? '✓' : idx + 1}
              </div>
              <span className={clsx(
                "text-[10px] text-center leading-tight",
                isActive ? "text-red-400 font-semibold" : "text-gray-600"
              )}>
                {stage.name}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
