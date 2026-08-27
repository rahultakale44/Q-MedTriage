import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './stages.css'
import './stages-redesign.css'
import './feature-extraction-compact.css'
import './pca-reference.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
