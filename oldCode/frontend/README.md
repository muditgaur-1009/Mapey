# Mapey Frontend

Modern Next.js 14 frontend for the Mapey career roadmap generator.

## Features

- ✅ Next.js 14 with App Router
- ✅ TypeScript for type safety
- ✅ TailwindCSS for styling
- ✅ Zustand for state management
- ✅ React Dropzone for file uploads
- ✅ React Markdown for content rendering
- ✅ React Hot Toast for notifications
- ✅ Responsive design with dark mode support
- ✅ API health monitoring

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/
│   ├── Header.tsx         # App header with API status
│   ├── RoadmapForm.tsx    # Input form
│   ├── RoadmapResults.tsx # Results display
│   └── LoadingSpinner.tsx # Loading state
├── lib/
│   ├── api.ts             # API client
│   └── store.ts           # Zustand store
└── types/
    └── api.ts             # TypeScript types
```

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Styling

The project uses TailwindCSS with a custom color scheme. Modify `tailwind.config.js` to customize.
