import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css' // Keep this for basic global styles if any
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)