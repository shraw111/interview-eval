# Interview Agent Frontend

Beautiful Next.js frontend for the Interview Agent evaluation system.

## Features

- **Modern UI**: Built with Next.js 14, TypeScript, and Tailwind CSS
- **Real-time Updates**: WebSocket integration for live evaluation progress
- **shadcn/ui Components**: Beautiful, accessible UI components
- **Form Validation**: Zod + react-hook-form for robust validation
- **Responsive Design**: Works on desktop, tablet, and mobile

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create a `.env.local` file:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── app/                     # Next.js App Router
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home page (evaluation form)
│   │   ├── evaluations/[id]/    # Results page
│   │   └── providers.tsx        # React Query provider
│   ├── components/
│   │   ├── ui/                  # shadcn/ui components
│   │   ├── evaluation/          # Evaluation-specific components
│   │   └── shared/              # Shared components
│   ├── lib/
│   │   ├── api/                 # API client (Axios)
│   │   ├── websocket/           # WebSocket hook
│   │   ├── hooks/               # Custom React hooks
│   │   ├── validation/          # Zod schemas
│   │   └── utils.ts             # Utility functions
│   └── types/                   # TypeScript types
└── public/                      # Static assets
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Key Technologies

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Beautiful UI components
- **TanStack Query** - Server state management
- **Axios** - HTTP client
- **Zod** - Schema validation
- **react-hook-form** - Form management
- **react-markdown** - Markdown rendering

## Features

### Evaluation Form
- Candidate information input
- Natural language rubric editor
- Interview transcript upload (paste or file)
- Real-time form validation

### Live Progress Tracking
- WebSocket connection for real-time updates
- Progress bar (0-100%)
- 4-agent status cards with live updates
- Token usage display per agent

### Results Display
- Beautiful evaluation journey accordion
- 4-step breakdown (Primary, Challenges, Calibrated, Decision)
- Metrics display (time, tokens, cost)
- Color-coded recommendation badges

## Development

The frontend connects to the FastAPI backend running on port 8000. Make sure the backend is running before starting the frontend.

See the main project README for full stack setup instructions.
